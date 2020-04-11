import * as THREE from 'three'
import normalizeWheel from 'normalize-wheel'
import Table from './Table'

class THREEController {
  constructor(options) {
    this.options = options
    this.staticfiles = options.staticfiles
    this.container = this.options.container
    this.cursor = this.options.cursor
    this.debug = this.options.debug || false
    this.width = this.container.offsetWidth
    this.height = this.container.offsetHeight
    this.camera = {}
    this.assets = {}
    this.scene = new THREE.Scene()
    this.group = new THREE.Group()
    this.mouse = new THREE.Vector3(0, 0, -0.2)
    this.direction = new THREE.Vector3(0, 0, 0)
    this.camera_position = new THREE.Vector3(0, 0, 0)
    this.drag_rotation = new THREE.Vector2(0, Math.PI / 6)
    this.rotation_direction = new THREE.Vector2(0, 0)
    this.camera_rotation = new THREE.Vector2(0, Math.PI / 6)
    this.cameraEasing = { x: 10, y: 1 }
    this.time = 0
    this.drag = false
    this.flag = 0
    this.assets = {}
    this.bancs = []

    this.init_environement()
    this.init_camera()
    this.init_lights()
    this.init_event()
    this.init_loader()
    this.initMaterialEvents()

    if (window.innerWidth < 960) {
      this.anim_in()
    }
  }

  anim_in() {
    this.drag_rotation.x = (2 * Math.PI) / 3

    if (window.innerWidth < 960) {
      this.mouse.z = -0.5
    }
  }

  init_lights() {
    let ambiant = new THREE.AmbientLight(0xffffff)
    this.scene.add(ambiant)
  }

  init_loader() {
    this.manager = new THREE.LoadingManager()

    this.assets.hdr = new THREE.TextureLoader(this.manager).load(this.staticfiles.hdr)
    this.assets.shadow = new THREE.TextureLoader(this.manager).load(this.staticfiles.shadow)

    this.assets.douglas_tex = new THREE.TextureLoader(this.manager).load(this.staticfiles.douglas)
    this.assets.chene_tex = new THREE.TextureLoader(this.manager).load(this.staticfiles.chene)
    this.assets.metal_tex = new THREE.TextureLoader(this.manager).load(this.staticfiles.metal)
    this.assets.none_tex = new THREE.TextureLoader(this.manager).load(this.staticfiles.none)

    this.assets.hdr.mapping = THREE.SphericalReflectionMapping

    this.manager.onProgress = (item, loaded, total) => {
      let progress = Math.round((loaded / total) * 100)
      if (progress == 100) {
        this.init()
      }
    }
  }

  init() {
    this.scene.add(this.group)

    this.table = new Table({
      scene: this.group,
      assets: this.assets,
      staticfiles: this.staticfiles,
      onChange: () => {
        this.cursor.triggerChange()
      },
    })

    this.cursor.init(this)
    this.initCheckboxOutside()
  }

  initCheckboxOutside() {
    let activeMaterial

    const checkbox = document.querySelector('#vernis')
    const materials = document.querySelectorAll('section.module .material')
    const metalMaterial = document.querySelector('section.module .metal-material')

    materials.forEach((material) => {
      if (material.classList.contains('active')) {
        activeMaterial = material.dataset.material
      }
    })

    if (checkbox) {
      checkbox.addEventListener('click', () => {
        if (checkbox.checked) {
          this.table.change_material('metal')
          this.bancs.forEach((banc) => banc.change_material('metal'))
          this.table.outside = true
          activeMaterial = this.table.active_desk

          materials.forEach((material) => material.classList.remove('active'))
          metalMaterial.classList.add('active')
        } else {
          this.table.outside = false
          this.table.change_material(activeMaterial)
          this.bancs.forEach((banc) => {
            banc.outside = false
            banc.change_material(activeMaterial)
          })

          metalMaterial.classList.remove('active')

          materials.forEach((material) => {
            if (material.dataset.material == activeMaterial) {
              material.classList.add('active')
            }
          })
        }
      })
    }
  }

  add_banc() {
    if (this.bancs.length === 0) {
      this.table.toggle_depth()
    }

    let banc_group = new THREE.Group()
    let position = 30
    if (this.bancs.length === 1) {
      position = -30
    }

    let banc = new Table({
      scene: banc_group,
      assets: this.assets,
      staticfiles: this.staticfiles,
      position: new THREE.Vector3(0, 0.01, position),
      width: 50,
      depth: 50,
      height: 80,
      onChange: () => {
        this.cursor.triggerChange()
      },
      onLoad: (banc) => {
        banc.changeSize(this.table.width / 2 - 25, 32, 45)
        banc.active_desk = this.table.active_desk
        banc.load_desk_material(1)
        banc.change_color(this.table.active_color)

        this.group.add(banc_group)
        this.bancs.push(banc)

        if (window.innerWidth > 960) {
          this.mouse.z = -0.3
        }
      },
    })
  }

  remove_banc() {
    if (this.bancs.length === 2) {
      this.bancs[1].scene.parent.remove(this.bancs[1].scene)
      let temp = this.bancs[0]
      this.bancs = null
      this.bancs = []
      this.bancs.push(temp)
    } else {
      this.remove_bancs()
    }
  }

  remove_bancs() {
    if (this.bancs.length > 0) {
      this.table.toggle_depth()
      let banc_count = document.querySelector('.banc-count')
      banc_count.textContent = 0
      for (var i = 0; i < this.bancs.length; i++) {
        this.bancs[i].scene.parent.remove(this.bancs[i].scene)
      }
      this.bancs = null
      this.bancs = []
    }
  }

  init_camera() {
    this.camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 1000)
    this.camera.position.z = 80
    this.camera.position.y = -10
  }

  init_environement() {
    // this.scene.fog = new THREE.FogExp2(0xfff2cc, 0.005)
    // this.scene.fog = new THREE.FogExp2(0xf6f8f9, 0.005)
    this.scene.fog = new THREE.FogExp2(0xf3f7fa, 0.0035)

    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
    })

    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5))
    this.renderer.setSize(this.width, this.height)

    this.container.appendChild(this.renderer.domElement)
  }

  init_event() {
    let that = this
    window.addEventListener(
      'resize',
      () => {
        that.width = this.container.offsetWidth
        that.height = this.container.offsetHeight
        that.camera.aspect = that.width / that.height
        that.camera.updateProjectionMatrix()
        that.renderer.setSize(that.width, that.height)
      },
      false
    )

    let last_mouse = { x: 0, y: 0 }

    this.container.addEventListener('mousemove', function (event) {
      that.mouse.x = (event.clientX / that.width - 0.5) * 2
      that.mouse.y = (event.clientY / that.height - 0.5) * 2

      let mouse_x = that.mouse.x - last_mouse.x
      let mouse_y = that.mouse.y - last_mouse.y

      if (that.drag) {
        that.drag_rotation.x += mouse_x * 1.5
        that.drag_rotation.y += mouse_y * 1.5
        that.drag_rotation.y = Math.min(Math.max(that.drag_rotation.y, Math.PI / 20), Math.PI / 4)
      }

      last_mouse.x = that.mouse.x
      last_mouse.y = that.mouse.y
    })

    this.container.addEventListener('mousedown', () => {
      this.drag = true
      this.container.classList.add('dragging')
    })

    window.addEventListener('mouseup', () => {
      this.drag = false
      this.container.classList.remove('dragging')
    })
  }

  initMaterialEvents() {
    const materials = document.querySelectorAll('section.module .material')
    materials.forEach((elem) =>
      elem.addEventListener('click', () => {
        if (elem.dataset.material != 'metal' && this.table.outside) {
          this.table.outside = false
          document.querySelector('#vernis').checked = false
          this.bancs.forEach((banc) => (banc.outside = false))
        }
        this.table.change_material(elem.dataset.material)
        this.bancs.forEach((banc) => banc.change_material(elem.dataset.material))
        materials.forEach((material) => material.classList.remove('active'))
        elem.classList.add('active')
      })
    )

    const colors = document.querySelectorAll('section.module .color-param')
    colors.forEach((elem) =>
      elem.addEventListener('click', () => {
        this.table.change_color(elem.dataset.color)
        this.bancs.forEach((banc) => banc.change_color(elem.dataset.color))
        colors.forEach((node) => node.classList.remove('active'))
        elem.classList.add('active')
      })
    )
  }

  update() {
    // camera
    this.direction.subVectors(this.mouse, this.camera_position)
    this.direction.multiplyScalar(0.06)
    this.camera_position.addVectors(this.camera_position, this.direction)

    this.rotation_direction.subVectors(this.drag_rotation, this.camera_rotation)
    this.rotation_direction.multiplyScalar(0.04)
    this.camera_rotation.addVectors(this.camera_rotation, this.rotation_direction)

    if (this.table != undefined) {
      this.table.update()
    }
    for (var i = 0; i < this.bancs.length; i++) {
      this.bancs[i].update()
    }

    this.group.rotation.y = this.camera_rotation.x * 2
    this.group.rotation.x = this.camera_rotation.y

    this.group.scale.set(1 + this.camera_position.z, 1 + this.camera_position.z, 1 + this.camera_position.z)

    this.camera.lookAt(new THREE.Vector3(0, 5, 0))

    this.renderer.render(this.scene, this.camera)
  }
}

export default THREEController
