import Contact_form from './contact_form.class'

class Popins {
    constructor(list) {

        this.background = document.querySelector('.popin-background')
        this.activated = list

        this.popin_thank_you = document.querySelector('.thank-you')

        for (var i = 0; i < this.activated.length; i++) {
          this[this.activated[i]]()
        }

        this.active_popin = null

        window.POPIN = this

        this.init_event_background()

    }

    init_event_background(){
        this.background.addEventListener('click', ()=>{
            if (this.active_popin !== null) {
                this.hide(this.active_popin)
            }
        })
    }

    display(name){
        this.background.classList.add('active')
        this["popin_" + name].classList.remove('hidden')
        setTimeout( () => {
          this["popin_" + name].classList.add('active')
        }, 10)
        this.active_popin = name
    }

    hide(name){
        this["popin_" + name].classList.remove('active')
        setTimeout( () => {
          this["popin_" + name].classList.add('hidden')
          this.background.classList.remove('active')
          this.active_popin = null
        }, 500)
    }

    basket(){
        let popin_basket = document.querySelector('.popin.basket')
        this.popin_basket = popin_basket

        popin_basket.querySelector('.return').addEventListener('click', (e)=>{
            this.hide('basket')
        })

        popin_basket.querySelector('.checkout').addEventListener('click', (e)=>{
            e.preventDefault()
            window.location = window.SETTINGS.checkout_url
        })
    }

    contact(){
        let popin_contact = document.querySelector('.contact-popin')
        this.popin_contact = popin_contact

        new Contact_form(popin_contact.querySelector('form'))

        let wrappers = popin_contact.querySelectorAll('.input-wrapper')
        for (var i = 0; i < wrappers.length; i++) {
            wrappers[i].addEventListener('focusin', function () {
                this.classList.add('active')
            })

            wrappers[i].addEventListener('focusout', function () {
                console.log();
                if (this.querySelector('input')) {
                    if (this.querySelector('input').value.length === 0) {
                      this.classList.remove('active')
                    }
                } else if (this.querySelector('textarea')) {
                    if (this.querySelector('textarea').value.length === 0) {
                      this.classList.remove('active')
                    }
                }
            })
        }

        popin_contact.querySelector('.cross').addEventListener('click', (e)=>{
            this.hide('contact')
        })
    }

    cgu() {

        let popin_cgu = document.querySelector('.cgu')
        this.popin_cgu = popin_cgu

        let popin_cgu_button = document.querySelector('.cgu-button')
        let popin_cgu_cross = document.querySelector('.cgu-cross')

        popin_cgu_button.addEventListener('click', (e)=>{
            e.preventDefault()
            this.background.classList.add('active')
            popin_cgu.classList.remove('hidden')
            popin_cgu.querySelector('.wrapper').innerHTML = "loading"
            let xmlhttp = new XMLHttpRequest()
            xmlhttp.onreadystatechange = () => {
                if (xmlhttp.readyState == XMLHttpRequest.DONE ) {
                   if (xmlhttp.status == 200) {
                       popin_cgu.querySelector('.wrapper').innerHTML = xmlhttp.responseText
                   }
                   else {
                      popin_cgu.querySelector('.wrapper').innerHTML = "Une erreur s'est produite... Contactez-nous pour de plus amples informations."
                   }
                }
            }
            xmlhttp.open("GET", window.SETTINGS.cgu_url, true)
            xmlhttp.send()
            setTimeout(() => {
                popin_cgu.classList.add('active')
            }, 10)
        })

        popin_cgu_cross.addEventListener('click', (e)=>{
            this.background.classList.remove('active')
            popin_cgu.classList.remove('active')
            setTimeout(() => {
                popin_cgu.classList.add('hidden')
            }, 10)
        })
    }

    a_propos() {

        let popin_cgu = document.querySelector('.cgu')
        this.popin_cgu = popin_cgu

        let popin_cgu_button = document.querySelector('.a-propos-button')
        let popin_cgu_cross = document.querySelector('.cgu-cross')

        popin_cgu_button.addEventListener('click', (e) => {
            e.preventDefault()
            this.background.classList.add('active')
            popin_cgu.classList.remove('hidden')
            popin_cgu.querySelector('.wrapper').innerHTML = "loading"
            let xmlhttp = new XMLHttpRequest()
            xmlhttp.onreadystatechange = () => {
                if (xmlhttp.readyState == XMLHttpRequest.DONE) {
                    if (xmlhttp.status == 200) {
                        popin_cgu.querySelector('.wrapper').innerHTML = xmlhttp.responseText
                    }
                    else {
                        popin_cgu.querySelector('.wrapper').innerHTML = "Une erreur s'est produite... Contactez-nous pour de plus amples informations."
                    }
                }
            }
            xmlhttp.open("GET", window.SETTINGS.a_propos_url, true)
            xmlhttp.send()
            setTimeout(() => {
                popin_cgu.classList.add('active')
            }, 10)
        })

        popin_cgu_cross.addEventListener('click', (e) => {
            this.background.classList.remove('active')
            popin_cgu.classList.remove('active')
            setTimeout(() => {
                popin_cgu.classList.add('hidden')
            }, 10)
        })
    }

    checkout_cgu() {

        let popin_cgu = document.querySelector('.cgu')
        this.popin_checkout_cgu = popin_cgu

        let xmlhttp = new XMLHttpRequest()
        xmlhttp.onreadystatechange = () => {
            if (xmlhttp.readyState == XMLHttpRequest.DONE ) {
               if (xmlhttp.status == 200) {
                   popin_cgu.querySelector('.wrapper').innerHTML = xmlhttp.responseText
               }
               else {
                  popin_cgu.querySelector('.wrapper').innerHTML = "Une erreur s'est produite... Contactez-nous pour de plus amples informations."
               }
            }
        }
        xmlhttp.open("GET", window.SETTINGS.cgu_url, true)
        xmlhttp.send()

        popin_cgu.querySelector('.cross').addEventListener('click', (e)=>{
            this.hide('checkout_cgu')
        })
    }

    more_color(){
      let popin_more_color = document.querySelector('.more')
      let more_color_open = false

      popin_more_color.addEventListener('click', function(){
          setTimeout( () => {
            if (more_color_open){
              this.classList.remove('active')
              more_color_open = false
            } else {
              this.classList.add('active')
              more_color_open = true
            }
          }, 10)
      })
      document.querySelector('section.module .params').addEventListener('click', function(){
          if (more_color_open) {
              popin_more_color.classList.remove('active')
              setTimeout( () => {
                more_color_open = false
              }, 20)
          }
      })
    }

    gallery(){
      let gallery_launcher = document.querySelector('.gallery-launcher')
      let gallery = document.querySelector('section.gallery')
      let gallery_right = document.querySelector('section.gallery .right')
      let gallery_left = document.querySelector('section.gallery .left')
      let active_gallery_index = 0

      gallery_launcher.addEventListener('click', function(){
          gallery.classList.add('active')
      })
      let photos_gallery = document.querySelectorAll('section.gallery li')
      for (var i = 0; i < photos_gallery.length; i++) {
          photos_gallery[i].classList.remove('active')
      }
      photos_gallery[active_gallery_index].classList.add('active')

      gallery_right.addEventListener('click', function(){
          for (var i = 0; i < photos_gallery.length; i++) {
              photos_gallery[i].classList.remove('active')
          }
          if (active_gallery_index < photos_gallery.length - 1) {
              active_gallery_index ++
          } else {
              active_gallery_index = 0
          }
          photos_gallery[active_gallery_index].classList.add('active')
      })

      gallery_left.addEventListener('click', function(){
          for (var i = 0; i < photos_gallery.length; i++) {
              photos_gallery[i].classList.remove('active')
          }
          if (active_gallery_index > 0) {
              active_gallery_index--
          } else {
              active_gallery_index = photos_gallery.length - 1
          }
          photos_gallery[active_gallery_index].classList.add('active')
      })

      gallery.querySelector('.background').addEventListener('click', function(){
          gallery.classList.remove('active')
      }, false)
    }
}
export default Popins
