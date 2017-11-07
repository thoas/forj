let yearHasChanged = false
let mounthHasChanged = false

class Payment_form {

    constructor() {

          this.form = document.querySelector('form.main')

          this.init_inputs()
          this.init_submit()
          this.check_number()
          this.check_crypto()
          this.updateSelect()

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
    }

    check_number(){
        this.form.querySelector('#number').addEventListener('change', ()=>{
            let number = this.form.querySelector('#number').value
            if (number.match(/\S+@\S+\.\S+/)) {
              this.number_checked = true
              this.form.querySelector('label.number').parentNode.classList.remove('error')
            //   this.form.querySelector('label.number').textContent = "Adresse number"
            } else if(number.length > 0) {
                // this.form.querySelector('label.number').textContent = "Format incorrect"
              this.form.querySelector('label.number').parentNode.classList.add('error')
              setTimeout( ()=> {
                this.form.querySelector('#number').parentNode.classList.remove('filled')
              }, 102)
            }
        })
    }

    check_crypto(){
        this.form.querySelector('#crypto').addEventListener('change', ()=>{
            let crypto = this.form.querySelector('#crypto').value
            if (crypto.match(/^[0-9]{3,4}$/)) {
              this.crypto_checked = true
              this.form.querySelector('label.crypto').parentNode.classList.remove('error')
            } else if(crypto.length > 0) {
              this.form.querySelector('label.crypto').parentNode.classList.add('error')
              setTimeout( ()=> {
                this.form.querySelector('#crypto').parentNode.classList.remove('filled')
              }, 102)
            }
        })
    }

    updateSelect(){
        let mounth = document.querySelector('#mounth')
        let mounthTextFeeback = document.querySelector('.mounthFeedBack')
        mounth.addEventListener('change', ()=>{
            mounthHasChanged = true
            mounthTextFeeback.textContent = mounth.value
        })

        let year = document.querySelector('#year')
        let yearTextFeeback = document.querySelector('.yearFeedBack')
        year.addEventListener('change', ()=>{
            yearHasChanged = true
            yearTextFeeback.textContent = year.value
        })
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

            // let del = document.createElement('p')
            // del.classList.add('delete')
            // del.innerHTML = "SUPPRIMER"
            // container.appendChild(del)

            let price = document.createElement('p')
            price.classList.add('price')
            price.innerHTML = item.price + ",00 €"
            container.appendChild(price)

            basket_container.appendChild(container)

            let that = this
            // del.addEventListener('click', function(evt) {
            //     let index = JSON.parse(this.parentNode.querySelector('.index').textContent)
            //     window.STORAGE.basket.remove_from_basket(index)

            //     this.parentNode.classList.add('disapering')
            //     setTimeout( ()=> { this.parentNode.classList.add('hidden') }, 500)
            //     setTimeout( ()=> { that.update_basket() }, 1000)

            // })

        }

        let total_price = document.querySelector('#total_price')
        total_price.value = total

        let total_dom = document.querySelector('#total')
        total_dom.textContent = total + ",00 €"

    }

    init_submit(){
        this.form.addEventListener('submit', (evt)=> {

            document.querySelector('.error-label').classList.remove('active')

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

            document.querySelector('.mounthFeedBack').classList.remove('error')
            document.querySelector('.yearFeedBack').classList.remove('error')

            if (errors.length === 0 && required_filled && yearHasChanged && mounthHasChanged) {
               
            } else {
                evt.preventDefault()
                document.querySelector('.error-label').classList.add('active')
                
                if (!mounthHasChanged) {
                    document.querySelector('.mounthFeedBack').classList.add('error')
                }
                
                if (!yearHasChanged) {
                    document.querySelector('.yearFeedBack').classList.add('error')
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
export default Payment_form
