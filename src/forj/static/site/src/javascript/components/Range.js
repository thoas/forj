import Draggable from 'gsap/Draggable'
import * as TweenMax from 'gsap'
import normalizeWheel from 'normalize-wheel'

class Range {
  constructor(options = {}) {
    this.presets = document.querySelectorAll('section.module .presets-selector')
    this.custom = document.querySelector('section.module .custom-selector')
    this.ranges = document.querySelectorAll('section.module .cursor-container')
    this.depth = options.depth || 80
    this.width = options.width || 140
    this.height = options.height || 74
    this.onChange = options.onChange

    this.basket = null
    this.need_roll = false
    this.alreadyScrolled = false

    this.controller = null
    this.table = null
  }

  init(controller) {
    this.controller = controller
    this.table = controller.table

    this.initPresets()
    this.init_ranges()
    this.table.changeSize(this.width, this.depth, this.height)
    this.update_range()
    this.init_bancs()
    this.triggerChange()
    this.initScroll()
    this.init_roll_down()
  }

  triggerChange() {
    if (this.onChange !== undefined) {
      this.onChange()
    }
  }

  init_roll_down() {
    let list = document.querySelector('.presets')
    let button = document.querySelector('.presets .mobile-dropdown')
    let shifter = document.querySelector('.shifter')

    let items = [...list.querySelectorAll('li')]
    let height = (items.length + 1) * items[0].offsetHeight
    let elementHeight = items[0].offsetHeight

    let expanded = false

    let check_size = () => {
      if (window.innerWidth < 1180) {
        this.need_roll = true
      } else {
        this.need_roll = false
        expanded = false
        shifter.style.transform = 'translate(0,0)'
        shifter.style.webkitTransform = 'translate(0,0)'
      }
    }
    check_size()

    window.addEventListener('resize', () => {
      check_size()
    })

    button.addEventListener('click', () => {
      shifter.style.transform = 'translate(0,0)'

      if (!expanded) {
        list.style.height = height + 'px'
        expanded = true
      } else {
        list.style.height = '50px'
        expanded = false
      }
    })

    let that = this
    for (var i = 0; i < items.length; i++) {
      items[i].addEventListener('click', function() {
        if (that.need_roll) {
          list.style.height = '50px'
          expanded = false
          let offset = items.indexOf(this) * -64
          shifter.style.transform = 'translate(0,' + offset + 'px)'
          shifter.style.webkitTransform = 'translate(0,' + offset + 'px)'
        }
      })
    }
  }

  initScroll() {
    const scroll = () => {
      if (!this.alreadyScrolled) {
        document.body.classList.remove('fixed')
        setTimeout(function() {
          this.controller.anim_in()
        }.bind(this), 500)
      }

      const module = document.querySelector('.module')
      const distance = module.getBoundingClientRect().top

      TweenMax.to({ value: window.scrollY }, 1, {
        value: distance,
        ease: Expo.easeInOut,
        onStart: function() {},
        onUpdate: function() {
          window.scrollTo(0, this.target.value)
        },
        onComplete: () => {
          this.alreadyScrolled = true
        }
      })
    }

    document.querySelectorAll('.scroll-to').forEach(node => node.addEventListener('click', () => scroll()))

    let wheelFired = false
    let prevent = true
    window.addEventListener('mousewheel', e => {
      if (window.scrollY > 10 && !this.alreadyScrolled) {
        this.alreadyScrolled = true
        this.controller.anim_in()
        document.body.classList.remove('fixed')
        prevent = false
        return
      }
      if (prevent) {
        e.preventDefault()
        setTimeout(() => {
          prevent = false
        }, 1000)
      }
      const normalizedWheel = normalizeWheel(e)
      const wheel = normalizedWheel.spinY
      if (wheel > 0 && !this.alreadyScrolled && !wheelFired) {
        wheelFired = true
        scroll()
      }
    })
  }

  initPresets() {
    const bancsSelector = document.querySelector('section.module .bancs')
    const bancEnabled = document.querySelector('section.module .banc-enabled')

    this.presets.forEach(preset => preset.addEventListener('click', () => {
      const depth = preset.dataset.depth
      const width = preset.dataset.width
      const height = preset.dataset.height

      if (preset === bancEnabled) {
        bancsSelector.classList.add('active')
      } else {
        bancsSelector.classList.remove('active')
      }

      this.table.changeSize(width, depth, height)
      setTimeout(() => {
        if (window.innerWidth < 960) {
          this.controller.mouse.z = -0.5
        } else {
          this.controller.mouse.z = -0.2
        }
      }, 470)

      this.depth = depth
      this.width = width
      this.height = height
      this.update_range()
      this.update_bancs()

      this.presets.forEach(node => {
        node.classList.remove('selected')
        node.classList.add('active')
      })

      this.custom.classList.remove('selected')
      preset.classList.add('selected')

      this.controller.remove_bancs()
    }))
  }

  init_ranges() {
    this.draggables = []
    for (var i = 0; i < this.ranges.length; i++) {
      let range = this.ranges[i]
      let cursor = range.querySelector('.cursor')
      let min = JSON.parse(range.dataset.min)
      let max = JSON.parse(range.dataset.max)
      let type = range.dataset.type
      let bancs_selector = document.querySelector('section.module .bancs')
      let draggable = Draggable.create(cursor, {
        type: 'x',
        bounds: range,
        onDrag: () => {
          let ratio = draggable[0].x / draggable[0].maxX
          let size = Math.round(min + (max - min) * ratio)
          range.parentNode.querySelector('.value').textContent = size

          if (type === 'depth') {
            this.depth = size
          } else if (type === 'width') {
            this.width = size
          } else if (type === 'height') {
            this.height = size
          }
          this.table.changeSize(this.width, this.depth, this.height)
          for (var i = 0; i < this.controller.bancs.length; i++) {
            this.controller.bancs[i].changeSize(this.width - 25, 32, 45)
          }

          if (type === 'height') {
            this.controller.remove_bancs()
            this.update_bancs()
            bancs_selector.classList.remove('active')

            for (var i = 0; i < this.presets.length; i++) {
              this.presets[i].classList.remove('selected')
              this.presets[i].classList.remove('active')
            }
            this.custom.classList.add('selected')
          }
        },
        onRelease: () => {}
      })
      this.draggables.push(draggable[0])
    }
  }

  update_bancs() {
    let banc_count = document.querySelector('.banc-count')
    let add_banc = document.querySelector('.add-banc')
    let remove_banc = document.querySelector('.remove-banc')

    add_banc.classList.remove('disabled')
    remove_banc.classList.remove('disabled')

    if (this.controller.bancs.length === 2) {
      add_banc.classList.add('disabled')
    }
    if (this.controller.bancs.length === 0) {
      remove_banc.classList.add('disabled')
    }
  }

  init_bancs() {
    let banc_count = document.querySelector('.banc-count')
    let add_banc = document.querySelector('.add-banc')
    let remove_banc = document.querySelector('.remove-banc')

    add_banc.addEventListener('click', () => {
      let count = JSON.parse(banc_count.textContent)
      if (this.controller.bancs.length < 2) {
        this.controller.add_banc()
        this.triggerChange()
        count++
        banc_count.textContent = count
        if (this.controller.bancs.length === 2) {
          add_banc.classList.add('disabled')
        } else {
          add_banc.classList.remove('disabled')
          remove_banc.classList.remove('disabled')
        }
      }
    })
    remove_banc.addEventListener('click', () => {
      let count = JSON.parse(banc_count.textContent)
      if (this.controller.bancs.length > 0) {
        this.controller.remove_banc()
        this.triggerChange()
        count--
        banc_count.textContent = count
        if (this.controller.bancs.length === 0) {
          remove_banc.classList.add('disabled')
        } else {
          add_banc.classList.remove('disabled')
          remove_banc.classList.remove('disabled')
        }
      }
    })
  }

  update_range() {
    let ranges = []
    for (var i = 0; i < this.ranges.length; i++) {
      let range = this.ranges[i]
      ranges.push({
        min: JSON.parse(range.dataset.min),
        max: JSON.parse(range.dataset.max),
        type: range.dataset.type,
        cursor: range.querySelector('.cursor'),
        value: range.parentNode.querySelector('.value')
      })
    }

    this.depth = Math.min(Math.max(this.depth, ranges[0].min), ranges[0].max)
    this.width = Math.min(Math.max(this.width, ranges[1].min), ranges[1].max)
    this.height = Math.min(Math.max(this.height, ranges[2].min), ranges[2].max)

    let depth_ratio = (this.depth - ranges[0].min) / (ranges[0].max - ranges[0].min)
    let width_ratio = (this.width - ranges[1].min) / (ranges[1].max - ranges[1].min)
    let height_ratio = (this.height - ranges[2].min) / (ranges[2].max - ranges[2].min)

    let depth_pixel = Math.round(this.draggables[0].maxX * depth_ratio)
    let width_pixel = Math.round(this.draggables[1].maxX * width_ratio)
    let height_pixel = Math.round(this.draggables[2].maxX * height_ratio)

    TweenMax.to(ranges[0].cursor, 1, { x: depth_pixel, ease: Expo.easeInOut })
    TweenMax.to(ranges[1].cursor, 1, { x: width_pixel, ease: Expo.easeInOut })
    TweenMax.to(ranges[2].cursor, 1, { x: height_pixel, ease: Expo.easeInOut })

    let values = {
      depth: JSON.parse(ranges[0].value.textContent),
      width: JSON.parse(ranges[1].value.textContent),
      height: JSON.parse(ranges[2].value.textContent)
    }

    TweenMax.to(values, 1, {
      depth: this.depth,
      width: this.width,
      height: this.height,
      onUpdate: function() {
        ranges[0].value.textContent = Math.round(this.target.depth)
        ranges[1].value.textContent = Math.round(this.target.width)
        ranges[2].value.textContent = Math.round(this.target.height)
      }
    })
  }
}
export default Range
