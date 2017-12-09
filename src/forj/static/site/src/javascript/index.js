import * as TOOLS from './components/tools'
import THREEController from './components/THREEController'
import Range from './components/Range'
import StickyBar from './components/StickyBar'
import Slider from './components/Slider'
import Popins from './components/Popins'
import * as TweenMax from 'gsap'

const cursor = new Range({
  onChange: () => {
    let surface = cursor.table.width * cursor.table.depth / 40000
    surface = Math.max(surface, 1)

    let plateau_price
    if (cursor.table.active_desk === 'none') {
      plateau_price = window.SETTINGS.prices.sans_plateau
    } else if (cursor.table.active_desk === 'chene') {
      plateau_price = window.SETTINGS.prices.chene_plateau
    } else if (cursor.table.active_desk === 'metal') {
      plateau_price = window.SETTINGS.prices.metal
    } else {
      plateau_price = window.SETTINGS.prices.douglas
    }

    let laquage = 0
    if (cursor.table.outside) {
      laquage = window.SETTINGS.prices.traitement_exterieur
    }

    let prices = {
      time: window.SETTINGS.prices.main_d_oeuvre,
      plateau: plateau_price,
      vernis: window.SETTINGS.prices.vernis,
      acier: window.SETTINGS.prices.acier,
      laquage: laquage
    }

    let total = 42
    for (let key in prices) {
      if (!prices.hasOwnProperty(key)) continue
      prices[key] *= surface
      total += prices[key]
    }

    // Marge
    total *= 1.5
    // TVA
    total *= 1.2
    total = Math.ceil(total)

    for (var i = 0; i < cursor.controller.bancs.length; i++) {
      total += 250
    }

    let diplayed_price = {}
    diplayed_price.dom = document.querySelector('#price-value')
    diplayed_price.value = parseFloat(diplayed_price.dom.textContent).toFixed(2)

    let tween_price = TweenMax.to(diplayed_price, 1, {
      value: total,
      ease: Expo.easeInOut,
      onUpdate: () => {
        if (tween_price.target.value.toFixed) {
          diplayed_price.dom.textContent = tween_price.target.value.toFixed(2)
        }
      }
    })

    let infos = [
      {
        depth: document.querySelector('section.infos .depth'),
        width: document.querySelector('section.infos .width'),
        height: document.querySelector('section.infos .height'),
        active_desk: document.querySelector('section.infos .desk'),
        active_color: document.querySelector('section.infos .color')
      },
      {
        depth: document.querySelector('.basket .depth'),
        width: document.querySelector('.basket .width'),
        height: document.querySelector('.basket .height'),
        active_desk: document.querySelector('.basket .desk'),
        active_color: document.querySelector('.basket .color')
      }
    ]

    for (var i = 0; i < infos.length; i++) {
      for (let key in infos[i]) {
        if (!infos[i].hasOwnProperty(key)) continue
        if (key === 'depth' || key === 'width' || key === 'height') {
          infos[i][key].textContent = cursor.table[key] / 2 + ',00'
        } else {
          infos[i][key].textContent = cursor.table[key]
        }
      }
    }

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
