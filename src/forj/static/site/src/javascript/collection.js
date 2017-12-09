import CollectionCarousel from './components/CollectionCarousel'
import Slider from './components/Slider'

const carousel = new CollectionCarrousel()

document.querySelectorAll('.slider').forEach(node => {
  new Slider(node)
})
