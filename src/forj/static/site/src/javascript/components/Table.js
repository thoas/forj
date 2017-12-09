import * as THREE from 'three'
import * as TweenMax from 'gsap'

class Table {
  constructor(options) {
    this.scene = options.scene
    this.assets = options.assets
    this.position = options.position || new THREE.Vector3()

    this.depth = options.depth || 160
    this.width = options.width || 280
    this.height = options.height || 148

    this.feets = []
    this.frame_parts = []

    this.init()
    this.init_material()
    this.init_feets()
    this.init_frame()
    this.init_desk()
    this.init_floor()
    this.init_check_outside()
    this.load_frame_material(1)

    this.need_change_size = false
    this.outside = false
  }

  init() {
    this.group_frame = new THREE.Group()
    this.scene.add(this.group_frame)
    this.group_feets = new THREE.Group()
    this.scene.add(this.group_feets)
    this.scene.position.x = this.position.x
    this.scene.position.y = this.position.y
    this.scene.position.z = this.position.z

    this.params = {
      douglas: {
        reflectivity: 0.02,
        tex: 'douglas_tex',
        opacity: 1
      },
      chene: {
        reflectivity: 0.07,
        tex: 'chene_tex',
        opacity: 1
      },
      metal: {
        reflectivity: 0.12,
        tex: 'metal_tex',
        opacity: 1
      },
      none: {
        reflectivity: 0,
        tex: 'none_tex',
        opacity: 0
      },
      colors: {
        brut: 0xa0a0a0,
        noir: 0x262626,
        gris: 0x505050,
        blanc: 0xffffff,
        orange: 0xd43e1b,
        cyan: 0xa7dfd4,
        jaune: 0xfed147,
        'option-bleu-fonce': 0x115b77,
        'option-bleu': 0x0080c9,
        'option-beige': 0xbf7e48,
        'option-orange': 0xf57b02,
        'option-rose': 0xd93f71,
        'option-vert-fonce': 0x537452,
        'option-marron': 0x6d5723
      }
    }

    this.active_desk = 'douglas'
    this.active_color = 'brut'
  }

  init_material() {
    this.floor_material = new THREE.MeshPhongMaterial({
      color: '#FFFFFF'
    })

    this.shadow_material = new THREE.MeshBasicMaterial({
      map: this.assets.shadow,
      transparent: true,
      opacity: 0.15,
      depthTest: true,
      needsUpdate: true
    })
  }

  toggle_depth() {
    this.shadow_material.depthTest = !this.shadow_material.depthTest
  }

  load_frame_material() {
    let material = new THREE.MeshPhongMaterial({
      color: this.params.colors[this.active_color],
      shininess: 100,
      envMap: this.assets.hdr,
      reflectivity: 0.2,
      needsUpdate: true
    })
    for (var i = 0; i < this.group_feets.children.length; i++) {
      this.group_feets.children[i].traverse(function(child) {
        if (child instanceof THREE.Mesh && child.userData.color) {
          child.material = material
        }
      })
    }
    for (var i = 0; i < this.frame_parts.length; i++) {
      this.frame_parts[i].traverse(function(child) {
        if (child instanceof THREE.Mesh && child.userData.color) {
          child.material = material
        }
      })
    }
    if (this.active_desk === 'metal') {
      this.load_desk_material(1)
    }
  }

  load_desk_material(opacity) {
    let color = null
    if (this.active_desk === 'metal') {
      color = this.params.colors[this.active_color]
    }

    this.desk.material = new THREE.MeshPhongMaterial({
      color: color,
      map: this.assets[this.params[this.active_desk].tex],
      shininess: 100,
      envMap: this.assets.hdr,
      reflectivity: this.params[this.active_desk].reflectivity,
      transparent: true,
      needsUpdate: true,
      opacity: opacity
    })
  }

  init_feets() {
    this.feets_pos = [-1, -1, 1, -1, -1, 1, 1, 1]

    let feet_geom = new THREE.BoxBufferGeometry(0.8, 11, 0.8)
    for (var i = 0; i < 4; i++) {
      let pivot = new THREE.Object3D()
      let feet = new THREE.Mesh(feet_geom, this.frame_material)
      feet.userData.color = true
      pivot.add(feet)

      let sub_frame_geom = new THREE.BoxBufferGeometry(5.5, 0.42, 0.5)
      let sub_frame = new THREE.Mesh(sub_frame_geom, this.frame_material)
      sub_frame.position.y = 10.6
      sub_frame.userData.color = true
      pivot.add(sub_frame)

      pivot.position.x = this.feets_pos[i * 2] * 10
      pivot.position.z = this.feets_pos[i * 2 + 1] * 10
      feet.position.y = 5
      pivot.lookAt(new THREE.Vector3(0, -4, 0))

      sub_frame.rotation.x = -0.2657291252981319

      pivot.castShadow = true
      this.group_feets.add(pivot)
      this.feets.push(pivot)
    }
  }

  init_frame() {
    let frame_pos = [-1, -1, 1, -1, -1, 1, 1, 1]

    let frame_geom = new THREE.BoxBufferGeometry(20.5, 0.2, 0.5)
    let frame_geom_2 = new THREE.BoxBufferGeometry(16, 0.42, 0.1)

    for (var i = 0; i < 4; i++) {
      let pivot = new THREE.Object3D()
      let temp_frame = new THREE.Mesh(frame_geom, this.frame_material)
      let temp_frame_2 = new THREE.Mesh(frame_geom_2, this.frame_material)
      pivot.position.x = frame_pos[i * 2] * 10
      pivot.position.z = frame_pos[i * 2 + 1] * 10
      pivot.position.y = 10
      temp_frame.position.x = 10
      temp_frame.userData.color = true
      temp_frame_2.position.x = 10
      temp_frame_2.position.y = 0.2
      temp_frame_2.position.z = 0.25
      temp_frame_2.userData.color = true
      pivot.add(temp_frame)
      pivot.add(temp_frame_2)
      this.group_frame.add(pivot)
      this.frame_parts.push(pivot)
    }

    this.frame_parts[1].rotation.y = -Math.PI / 2
    this.frame_parts[2].rotation.y = Math.PI / 2
    this.frame_parts[3].rotation.y = -Math.PI
  }

  init_desk() {
    let desk_geom = new THREE.BoxBufferGeometry(20.5, 0.6, 20.5)
    this.desk = new THREE.Mesh(desk_geom, this.desk_material)
    this.desk.position.y = 10.5
    this.load_desk_material(1)

    this.scene.add(this.desk)
  }

  init_floor() {
    let plane = new THREE.Mesh(new THREE.PlaneBufferGeometry(1000, 1000), this.floor_material)
    plane.rotation.x = -Math.PI / 2
    this.scene.add(plane)

    this.shadow = new THREE.Mesh(new THREE.PlaneBufferGeometry(20.5 * 1.5, 20.5 * 1.5), this.shadow_material)
    this.shadow.rotation.x = -Math.PI / 2
    this.shadow.position.y = 0.01
    this.group_frame.add(this.shadow)
  }

  resize() {
    this.group_frame.scale.y = this.height / 100
    this.group_feets.scale.y = this.height / 100

    this.group_frame.scale.x = this.width / 100
    this.group_frame.scale.z = this.depth / 100

    for (var i = 0; i < 4; i++) {
      this.feets[i].position.x = this.feets_pos[i * 2] * 10 * this.width / 100
      this.feets[i].position.z = this.feets_pos[i * 2 + 1] * 10 * this.depth / 100
    }

    this.desk.position.y = 10 * this.height / 100 + 0.7
    this.desk.scale.x = this.width / 100
    this.desk.scale.z = this.depth / 100
  }

  change_material(mat) {
    if (!this.outside) {
      TweenMax.to(this.desk.material, 0.4, {
        opacity: 0,
        ease: Power1.ease,
        onComplete: () => {
          this.active_desk = mat
          this.load_desk_material(0)
        }
      })

      setTimeout(() => {
        TweenMax.to(this.desk.material, 0.4, {
          opacity: 1,
          ease: Power1.ease,
          onComplete: () => {
            window.STORAGE.CURSOR.update_price()
          }
        })
      }, 500)
    }
  }

  change_size(w, d, h) {
    w = Math.min(Math.max(w, 25), 200)
    d = Math.min(Math.max(d, 25), 120)
    h = Math.min(Math.max(h, 40), 120)

    this.need_change_size = true
    TweenMax.to(this, 1, {
      width: w * 2,
      depth: d * 2,
      height: h * 2,
      // ease: Elastic.easeOut.config(1, 0.3),
      ease: Expo.easeInOut,
      onComplete: () => {
        setTimeout(() => {
          this.need_change_size = false
          window.STORAGE.CURSOR.update_price()
        }, 10)
      }
    })
  }

  change_color(color) {
    this.active_color = color
    this.load_frame_material()
    window.STORAGE.CURSOR.update_labels()
  }

  init_check_outside() {
    let previous_mat = 'douglas'
    let checkbox = document.querySelector('#vernis')
    checkbox.addEventListener('click', () => {
      if (checkbox.checked) {
        this.change_material('metal')
        for (var i = 0; i < window.GL.bancs.length; i++) {
          window.GL.bancs[i].change_material('metal')
        }
        this.outside = true
        previous_mat = this.active_desk
        let materials = document.querySelectorAll('section.module .material')
        for (var i = 0; i < materials.length; i++) {
          materials[i].classList.remove('active')
        }
        document.querySelector('section.module .metal-material').classList.add('active')
      } else {
        this.outside = false
        this.change_material(previous_mat)
        for (var i = 0; i < window.GL.bancs.length; i++) {
          window.GL.bancs[i].outside = false
          window.GL.bancs[i].change_material(previous_mat)
        }
      }
    })
  }

  update() {
    if (this.need_change_size) {
      this.resize()
    }
  }
}
export default Table
