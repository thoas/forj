class Checkout_form {

    constructor() {

          this.form = document.querySelector('form.main')

          this.mail_checked     = false
          this.phone_checked    = false

          this.check_mail()
          this.check_confirmedmail()
          this.check_phone()
          this.init_inputs()
          this.check_zip()
          this.init_cgu()
          this.init_submit()

          setTimeout( () => {
            this.update_basket()
          }, 10)

    }

    init_inputs(){
        let wrappers = document.querySelectorAll('.input-wrapper')
        for (var i = 0; i < wrappers.length; i++) {
            wrappers[i].addEventListener('change', function () {
                setTimeout( ()=> {
                  for (var j = 0; j < wrappers.length; j++) {
                      if (wrappers[j].querySelector('input')) {
                          if (wrappers[j].querySelector('input').value.length > 0) {
                            wrappers[j].classList.add('filled')
                            wrappers[j].classList.add('active')
                          } else {
                            wrappers[j].classList.remove('filled')
                          }
                      }
                  }
                }, 100)
            })

            wrappers[i].addEventListener('focusin', function () {
                this.classList.add('active')
            })

            wrappers[i].addEventListener('focusout', function () {
                if (this.querySelector('input')) {
                    if (this.querySelector('input').value.length === 0) {
                      this.classList.remove('active')
                    } else {
                      this.classList.add('filled')
                    }
                }
            })
        }


        let check_box = document.querySelector('#facturation').addEventListener('change', function (){
            let facturation_adress = document.querySelector('.facturation-wrapper')
            if (this.checked) {
                facturation_adress.style.display = 'block'
                let inputs = facturation_adress.querySelectorAll('input')
                for (var i = 0; i < inputs.length; i++) {
                  inputs[i].classList.add('required')
                }
            } else {
                facturation_adress.style.display = 'none'
                let inputs = facturation_adress.querySelectorAll('input')
                for (var i = 0; i < inputs.length; i++) {
                  inputs[i].classList.remove('required')
                }
            }
        })
    }

    check_mail(){
        this.form.querySelector('#mail').addEventListener('change', ()=>{
            let mail = this.form.querySelector('#mail').value
            if (mail.match(/\S+@\S+\.\S+/)) {
              this.mail_checked = true
              this.form.querySelector('label.mail').parentNode.classList.remove('error')
            //   this.form.querySelector('label.mail').textContent = "Adresse mail"
            } else if(mail.length > 0) {
                // this.form.querySelector('label.mail').textContent = "Format incorrect"
              this.form.querySelector('label.mail').parentNode.classList.add('error')
              setTimeout( ()=> {
                this.form.querySelector('#mail').parentNode.classList.remove('filled')
              }, 102)
            }
        })
    }

    check_confirmedmail(){
        this.form.querySelector('#confirmeMail').addEventListener('change', ()=>{
            let confirmeMail = this.form.querySelector('#confirmeMail').value
            if (confirmeMail.match(/\S+@\S+\.\S+/) && confirmeMail === this.form.querySelector('#mail').value ) {
              this.confirmeMail_checked = true
              this.form.querySelector('label.confirmeMail').parentNode.classList.remove('error')
            //   this.form.querySelector('label.confirmeMail').textContent = "Adresse confirmée"
            } else if(confirmeMail.length > 0) {
                // this.form.querySelector('label.confirmeMail').textContent = "Format incorrect"
              this.form.querySelector('label.confirmeMail').parentNode.classList.add('error')
              setTimeout( ()=> {
                this.form.querySelector('#confirmeMail').parentNode.classList.remove('filled')
              }, 102)
            }
        })
    }

    check_phone(){
        this.form.querySelector('#phone').addEventListener('change', ()=>{
            let phone = this.form.querySelector('#phone').value
            if (phone.match(/^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im)) {
              this.phone_checked = true
              this.form.querySelector('label.phone').parentNode.classList.remove('error')
            //   this.form.querySelector('label.phone').textContent = "Téléphone"
            } else if(phone.length > 0) {
                // this.form.querySelector('label.phone').textContent = "Format incorrect"
              this.form.querySelector('label.phone').parentNode.classList.add('error')
              setTimeout( ()=> {
                this.form.querySelector('#phone').parentNode.classList.remove('filled')
              }, 102)
            }
        })
    }

    check_zip(){
        let zips = document.querySelectorAll('input.zip')
        for (var i = 0; i < zips.length; i++) {
            zips[i].addEventListener('change', function(){
                let zip = this.value
                if (zip.match(/^(([0-8][0-9])|(9[0-5]))[0-9]{3}$/)) {
                  this.parentNode.classList.remove('error')
                //   this.parentNode.querySelector('label').textContent = "Code postal"
                } else if(zip.length > 0) {
                    // this.parentNode.querySelector('label').textContent = "Format incorrect"
                  this.parentNode.classList.add('error')
                  setTimeout( ()=> {
                    this.parentNode.classList.remove('filled')
                  }, 102)
                }
            })
        }
    }

    update_basket(){

        let basket_hidden = document.querySelector('#basket_content')
        basket_hidden.value = JSON.stringify(window.STORAGE.basket)

        let total = 0

        let basket_container = document.querySelector('.article-container')
        basket_container.innerHTML = ""

        for (var i = 0; i < window.STORAGE.basket.items.length; i++) {

            let item = window.STORAGE.basket.items[i]

            total += item.price

            let container = document.createElement('div')
            container.classList.add('article')

            let dimenssions = document.createElement('div')
            dimenssions.classList.add('detail')
            dimenssions.innerHTML = "Dimensions : L." + item.width + " P." + item.depth + " H." + item.height
            container.appendChild(dimenssions)

            let desk = document.createElement('div')
            desk.classList.add('detail')
            desk.innerHTML = "Plateau : " + item.desk
            container.appendChild(desk)

            let color = document.createElement('div')
            color.classList.add('detail')
            color.innerHTML = "Couleur : " + item.color
            container.appendChild(color)

            if (item.bancs > 0) {
                let bancs = document.createElement('div')
                bancs.classList.add('detail')
                bancs.innerHTML = "Bancs : (" + item.bancs + ")"
                container.appendChild(bancs)
            }

            if (item.outside) {
                let outside = document.createElement('div')
                outside.classList.add('detail')
                outside.innerHTML = "Traitement extérieur"
                container.appendChild(outside)
            }

            let index = document.createElement('p')
            index.classList.add('index')
            index.style.display = 'none'
            index.innerHTML = i
            container.appendChild(index)

            let del = document.createElement('p')
            del.classList.add('delete')
            del.innerHTML = "SUPPRIMER"
            container.appendChild(del)

            let price = document.createElement('p')
            price.classList.add('price')
            price.innerHTML = item.price + ",00 €"
            container.appendChild(price)

            basket_container.appendChild(container)

            let that = this
            del.addEventListener('click', function(evt) {
                let index = JSON.parse(this.parentNode.querySelector('.index').textContent)
                window.STORAGE.basket.remove_from_basket(index)

                this.parentNode.classList.add('disapering')
                setTimeout( ()=> { this.parentNode.classList.add('hidden') }, 500)
                setTimeout( ()=> { that.update_basket() }, 1000)

            })

        }

        let total_price = document.querySelector('#total_price')
        total_price.value = total

        let total_dom = document.querySelector('#total')
        total_dom.textContent = total + ",00 €"

    }

    init_cgu(){
        let launcher = document.querySelector('.cgu-basket-launcher')
        launcher.addEventListener('click', (e)=> {
            e.preventDefault()
            window.POPIN.display('checkout_cgu')
        })
    }

    init_submit(){
        this.form.addEventListener('submit', (evt)=> {
            document.querySelector('.error-label').classList.remove('active')

            document.querySelector('.check-cgu-container label').classList.remove('error-cgu')

            let errors = document.querySelectorAll('.error')

            let required_filled = true
            let required = document.querySelectorAll('.required')
            for (var i = 0; i < required.length; i++) {
                if (required[i].value.length === 0) {
                    required_filled = false
                } else {
                    required[i].parentNode.classList.remove('error')
                }
            }

            let check_cgu = document.querySelector('#check-cgu')

            if (errors.length === 0 && required_filled && check_cgu.checked) {
                // evt.preventDefault()
            } else {
                evt.preventDefault()
                
                document.querySelector('.error-label').classList.add('active')

                if (!check_cgu.checked) {
                    document.querySelector('.check-cgu-container label').classList.add('error-cgu')
                }

                if (!required_filled) {
                  for (var i = 0; i < required.length; i++) {
                      if (required[i].value.length === 0) {
                          required[i].parentNode.classList.add('error')
                      }
                  }
                }
            }
        })
    }

}
export default Checkout_form
