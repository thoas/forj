import carousel from './components/Carousel'
import Slider from './components/Slider'

carousel(document.querySelectorAll('.carroussel'))

document.querySelectorAll('.slider').forEach(node => {
  new Slider(node)
})
