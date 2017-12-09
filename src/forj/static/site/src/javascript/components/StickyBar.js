class StickyBar {
  constructor(target) {
    this.target = target
    this.height_target = this.target.offsetHeight
    this.stick_ready = true
    this.unstick_ready = false
    this.stick_to = 'bottom'

    this.init()
    this.init_events()
    this.check_height()
  }

  init() {
    this.shadow_bar_after = document.createElement('div')
    this.shadow_bar_after.style.height = 0
    this.shadow_bar_after.style.width = 0
    this.shadow_bar_after.classList.add('shadow-bar')
    this.target.parentNode.insertBefore(this.shadow_bar_after, this.target.nextSibling)

    this.shadow_bar_before = document.createElement('div')
    this.shadow_bar_before.style.height = 0
    this.shadow_bar_before.style.width = 0
    this.shadow_bar_before.classList.add('shadow-bar')
    this.target.parentNode.insertBefore(this.shadow_bar_before, this.target.previousSibling)
  }

  init_events() {
    window.addEventListener('scroll', () => {
      this.check_height()
    })
  }

  check_height() {
    if (this.stick_to === 'top') {
      let bound_after = this.shadow_bar_after.getBoundingClientRect().top
      let bound_before = this.shadow_bar_before.getBoundingClientRect().top
      if (bound_after < this.height_target && this.stick_ready && !this.unstick_ready) {
        this.stick_ready = false
        this.stick(this.stick_to)
      } else if (bound_before > -this.height_target && !this.stick_ready && this.unstick_ready) {
        this.stick_ready = true
        this.unstick_ready = false
        this.unstick(this.stick_to)
      } else if (!this.stick_ready && !this.unstick_ready && bound_before > 0) {
        this.unstick_ready = true
      } else if (!this.stick_ready && this.unstick_ready && bound_before < 0) {
        this.stick_ready = true
      }
    } else {
      let bound_after = this.shadow_bar_after.getBoundingClientRect().bottom
      let bound_before = this.shadow_bar_before.getBoundingClientRect().bottom
      if (bound_after < window.innerHeight && this.stick_ready && !this.unstick_ready) {
        this.stick_ready = false
        this.stick(this.stick_to)
      }
    }
  }

  stick(anchor) {
    if (anchor === 'top') {
      this.shadow_bar_after.style.height = this.height_target + 'px'
    }
    this.target.style.position = 'fixed'
    this.target.style[anchor] = '0'
    this.target.style.left = '0'
    this.target.style.width = '100%'
    this.target.style.zIndex = '10'
    this.target.style.borderTop = '1px solid #d3d5d6'
  }

  unstick() {
    this.shadow_bar_after.style.height = '0'
    this.target.style.position = 'inherit'
    this.target.style.top = 'auto'
    this.target.style.bottom = 'auto'
    this.target.style.left = 'auto'
    this.target.style.width = 'auto'
    this.target.style.zIndex = 'auto'
  }
}
export default StickyBar
