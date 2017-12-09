import * as TOOLS from './components/tools'
import THREEController from './components/THREEController'
import Range from './components/Range'
import StickyBar from './components/StickyBar'
import Slider from './components/Slider'
import CollectionCarousel from './components/CollectionCarousel'
import Popins from './components/Popins'

let three

if (document.body.classList.contains('main')) {
  const cursor = new Range()
  three = new THREEController({
    container: document.querySelector('.webgl'),
    cursor: cursor,
    staticfiles: window.SETTINGS.staticfiles,
  })

  new StickyBar(document.querySelector('section.infos'))
  const popins = new Popins(['more_color', 'gallery', 'basket'])

  document.querySelector('#add-to-basket').addEventListener('click', e => {
    e.preventDefault()
    popins.display('basket')
  })
} else if (document.body.classList.contains('collection')) {
  new CollectionCarrousel()
}

document.querySelectorAll('.slider').forEach(node => {
  new Slider(node)
})

const hamburger = document.querySelector('.hamburger')
const mobileNav = document.querySelector('nav')
hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('active')
  mobileNav.classList.toggle('active')
})

const animate = () => {
  requestAnimationFrame(animate)

  // Updating components
  if (three !== undefined && three.renderer != undefined) {
    three.update()
  }
}

animate()
