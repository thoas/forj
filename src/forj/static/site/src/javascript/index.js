import * as axios from 'axios'
import * as TOOLS from './components/tools'
import THREEController from './components/THREEController'
import Range from './components/Range'
import StickyBar from './components/StickyBar'
import Slider from './components/Slider'
import Popins from './components/Popins'
import * as TweenMax from 'gsap'
import numeral from './format'

// formatProductReference formats the current selection in a product reference
// readable by the server
const formatProductReference = (cursor) => {
  let criterias = []

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

  return [
    [...criterias, `LO(${cursor.width})`, `LA(${cursor.depth})`, `H(${cursor.height})`].join('-'),
    ...cursor.controller.bancs.map((banc) =>
      ['T(BANC)', `LO(${cursor.width - 25 <= 25 ? 25 : cursor.width - 25})`, ...criterias, 'LA(28)', 'H(45)'].join('-')
    ),
  ]
}

const cursor = new Range({
  onChange: () => {
    const referenceList = formatProductReference(cursor)
    console.log('Product reference: ', referenceList.join(', '))

    var params = new FormData()
    params.append('action', 'detail')
    referenceList.forEach((reference) => params.append('reference', reference))

    axios.post(window.SETTINGS.urls.cart, params).then((res) => {
      const total = parseFloat(parseInt(res.data.total, 10) / 100.0)
      const priceNode = document.querySelector('#price-value')

      let price = {
        dom: priceNode,
        value: parseFloat(priceNode.textContent).toFixed(2),
      }

      let tweenPrice = TweenMax.to(price, 1, {
        value: total,
        ease: Expo.easeInOut,
        onUpdate: () => {
          if (tweenPrice.target.value.toFixed) {
            price.dom.textContent = numeral(tweenPrice.target.value).format('0.00')
          }
        },
      })
    })

    const ops = [
      [document.querySelectorAll('section.infos .depth, .basket .depth'), (elem) => (elem.textContent = cursor.depth)],
      [document.querySelectorAll('section.infos .width, .basket .width'), (elem) => (elem.textContent = cursor.width)],
      [
        document.querySelectorAll('section.infos .height, .basket .height'),
        (elem) => (elem.textContent = cursor.height),
      ],
      [
        document.querySelectorAll('section.infos .desk, .basket .desk'),
        (elem) => (elem.textContent = cursor.table.active_desk),
      ],
      [
        document.querySelectorAll('section.infos .color, .basket .color'),
        (elem) => (elem.textContent = cursor.table.active_color),
      ],
    ]
    ops.forEach((entry) => entry[0].forEach((elem) => entry[1](elem)))

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
  },
})

const container = document.querySelector('.webgl')
let three

if (container) {
  three = new THREEController({
    container: container,
    cursor: cursor,
    staticfiles: window.SETTINGS.staticfiles,
  })
}

const stickybar = document.querySelector('section.infos')
if (stickybar) {
  new StickyBar(stickybar)
}

const popin = document.querySelector('.popin-background')
let popins
if (popin) {
  popins = new Popins(popin, ['more_color', 'gallery', 'basket'])
}

const basketBtn = document.querySelector('#add-to-basket')
if (basketBtn) {
  basketBtn.addEventListener('click', (e) => {
    e.preventDefault()

    const referenceList = formatProductReference(cursor)

    var params = new FormData()
    params.append('action', 'add')
    referenceList.forEach((reference) => params.append('reference', reference))

    axios.post(window.SETTINGS.urls.cart, params).then((res) => {
      popins.display('basket')

      const sum = res.data.items.map((entry) => entry.quantity).reduce((a, b) => a + b, 0)

      document.querySelectorAll('.cart-counter').forEach((elem) => (elem.textContent = `(${sum})`))
    })
  })
}

document.querySelectorAll('.slider').forEach((node) => new Slider(node))

const animate = () => {
  requestAnimationFrame(animate)

  // Updating components
  if (three && three.renderer != undefined) {
    three.update()
  }
}

animate()
