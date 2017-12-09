import * as axios from 'axios'
import * as TOOLS from './components/tools'
import THREEController from './components/THREEController'
import Range from './components/Range'
import StickyBar from './components/StickyBar'
import Slider from './components/Slider'
import Popins from './components/Popins'
import * as TweenMax from 'gsap'

// formatProductReference formats the current selection in a product reference
// readable by the server
const formatProductReference = cursor => {
  let criterias = [];

  if (cursor.table.outside) {
      criterias.push('P(ACIEREXT)')
  } else {
    if (cursor.table.active_desk === 'chene') {
      criterias.push('P(BRUT)')
    } else if (cursor.table.active_desk === 'metal') {
      criterias.push('P(ACIER)')
    } else if (cursor.table.active_desk === 'douglas') {
      criterias.push('P(AGLO)')
    }
  }

  criterias.push(`R(${cursor.table.active_color.toUpperCase()})`)
  criterias.push(`LA(${cursor.depth})`)
  criterias.push(`LO(${cursor.width})`)
  criterias.push(`H(${cursor.height})`)

  return criterias.join('-')
}

const cursor = new Range({
  onChange: () => {
    const reference = formatProductReference(cursor)
    console.log(`Product reference: ${reference}`)

    var params = new URLSearchParams()
    params.append('action', 'detail')
    params.append('reference', reference)

    axios.post(window.SETTINGS.urls.cart, params).then(res => {
      const total = parseFloat(res.data.total_formatted)
      const priceNode = document.querySelector('#price-value')

      let price = {
        dom: priceNode,
        value: parseFloat(priceNode.textContent).toFixed(2)
      }

      let tweenPrice = TweenMax.to(price, 1, {
        value: total,
        ease: Expo.easeInOut,
        onUpdate: () => {
          if (tweenPrice.target.value.toFixed) {
            price.dom.textContent = tweenPrice.target.value.toFixed(2)
          }
        }
      })
    })

    const ops = [
      [document.querySelectorAll('section.infos .depth, .basket .depth'), (elem) => elem.textContent = cursor.depth],
      [document.querySelectorAll('section.infos .width, .basket .width'), (elem) => elem.textContent = cursor.width],
      [document.querySelectorAll('section.infos .height, .basket .height'), (elem) => elem.textContent = cursor.height],
      [document.querySelectorAll('section.infos .desk, .basket .desk'), (elem) => elem.textContent = cursor.table.active_desk],
      [document.querySelectorAll('section.infos .color, .basket .color'), (elem) => elem.textContent = cursor.table.active_color],
    ]
    ops.forEach(entry => entry[0].forEach(elem => entry[1](elem)))

    let outside = document.querySelector('section.infos .outside')
    if (cursor.table.outside) {
      outside.innerHTML = '<br>Traitement extérieur'
    } else {
      outside.textContent = ''
    }

    let bancs = document.querySelector('section.infos .bancs')
    if (cursor.controller.bancs.length > 0) {
      bancs.textContent = '(' + cursor.controller.bancs.length + ')'
    } else {
      bancs.textContent = '(0)'
    }

    let outside_popin = document.querySelector('.basket .outside')
    if (cursor.table.outside) {
      outside_popin.innerHTML = '<br>Traitement extérieur'
    } else {
      outside_popin.textContent = ''
    }

    let bancs_popin = document.querySelector('.basket .bancs')
    if (cursor.controller.bancs.length > 0) {
      bancs_popin.textContent = '(' + cursor.controller.bancs.length + ')'
    } else {
      bancs_popin.textContent = '(0)'
    }
  }
})

const three = new THREEController({
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
  if (three.renderer != undefined) {
    three.update()
  }
}

animate()
