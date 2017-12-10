import carousel from './components/Carousel'
import Slider from './components/Slider'

carousel(document.querySelectorAll('.carousel'))

document.querySelectorAll('.slider').forEach(node => new Slider(node))
