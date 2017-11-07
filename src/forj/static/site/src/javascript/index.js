import * as TOOLS             from './components/tools.class'
import THREE_Controller       from './components/THREE_Controller.class'
import Range                  from './components/range.class'
import Sticky_bar             from './components/sticky_bar.class'
import Slider                 from './components/slider.class'
import Popins                 from './components/popins.stuff'
import Basket                 from './components/basket.class'
import Checkout_form          from './components/checkout_from.class'
import Payment_form           from './components/payment_from.class'
import Collection_Carroussel  from './components/collection_carroussel'

// let framecounter = new TOOLS.FrameRateUI()
// framecounter.hide()

let three = {}
if (document.body.classList.contains('main')) {

    three         = new THREE_Controller({ container: document.querySelector('.webgl')})
    let range     = new Range()
    let sticky    = new Sticky_bar(document.querySelector('section.infos'))

    let sliders = document.querySelectorAll('.slider')
    for (var i = 0; i < sliders.length; i++) {
        let carroussel = new Slider(sliders[i])
    }

    new Popins(["cgu", "more_color", "gallery", "contact", "basket", "a_propos"])

    // Mobile menu activation

    let hamburger = document.querySelector('.hamburger')
    let nav_mobile = document.querySelector('nav')

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active')
        nav_mobile.classList.toggle('active')
    })

} else if (document.body.classList.contains('checkout')) {

    new Checkout_form()
    new Popins(["checkout_cgu", "a_propos"])
    
} else if (document.body.classList.contains('payment')) {
    
    new Payment_form()
    new Popins(["checkout_cgu", "a_propos"])

} else if (document.body.classList.contains('collection')) {

    new Collection_Carroussel()
    new Popins(["cgu"])
    let sliders = document.querySelectorAll('.slider')
    for (var i = 0; i < sliders.length; i++) {
        let carroussel = new Slider(sliders[i])
    }

    // Mobile menu activation

    let hamburger = document.querySelector('.hamburger')
    let nav_mobile = document.querySelector('nav')

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active')
        nav_mobile.classList.toggle('active')
    })

} else if (!document.body.classList.contains('success')) {
    let sliders = document.querySelectorAll('.slider')
    for (var i = 0; i < sliders.length; i++) {
        let carroussel = new Slider(sliders[i])
    }
    new Popins(["cgu", "contact", "a_propos"])
}

new Basket()


// start animating
animate();

function animate() {
    requestAnimationFrame(animate);

    // Updating components
    if (three.renderer != undefined) { three.update() }
    // framecounter.update()

}
