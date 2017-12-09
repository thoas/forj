const carousel = (target) => {
  const resetActive = (el) => {
    el.querySelectorAll('li').forEach(node => node.classList.remove('active'))
  }

  const init = (el) => {
    const arrowRight = el.querySelector('.arrow.right')
    const arrowLeft = el.querySelector('.arrow.left')
    const children = el.querySelectorAll('li')

    let pause = false
    let activeElement = 0
    resetActive(el)

    children[0].classList.add('active')

    let timer = setTimeout(function() {}, 0)

    arrowLeft.addEventListener('click', evt => {
      resetActive(el)
      activeElement <= 0 ? (activeElement = children.length - 1) : activeElement--
      children[activeElement].classList.add('active')
      if (evt !== undefined) {
        return
      }
      pause = true
      clearTimeout(timer)
      timer = setTimeout(() => {
        pause = false
      }, 5000)
    })

    arrowRight.addEventListener('click', evt => {
      resetActive(el)
      activeElement >= children.length - 1 ? (activeElement = 0) : activeElement++
      children[activeElement].classList.add('active')
      if (evt !== undefined) {
        return
      }
      pause = true
      clearTimeout(timer)
      timer = setTimeout(() => {
        pause = false
      }, 5000)
    })

    setInterval(function() {
      if (!pause) {
        arrowRight.click()
      }
    }, 3000 + Math.round(Math.random() * 2000))
  }

  target.forEach(node => init(node))
}

export default carousel
