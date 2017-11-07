// TODO append data with your ID in the formData 'this.data'

class Contact_form {

    constructor(form) {

          this.form = form
          this.data = new FormData()

          this.init()
          this.init_event()

    }

    init(){
        let launcher = document.querySelector('.popin_contact_launcher')
        launcher.addEventListener('click', function(e){
            e.preventDefault()
            window.POPIN.display('contact')
        })
    }

    init_event(){
        this.form.addEventListener('submit', (e)=>{
            e.preventDefault()
            this.build_form()
        })
    }

    build_form(){

        let mail = this.form.querySelector('#contact-mail').value
        let phone = this.form.querySelector('#contact-phone').value
        let message = this.form.querySelector('#contact-asking').value
        let progress = this.form.querySelector('.progress')
        let valid_inputs = 0

        this.userData = {
          mail: mail,
          phone: phone,
          message: message,
        }

        if (phone.match(/^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im)) {
            this.data.append("phone", phone)
            valid_inputs++
        } else {
            this.form.querySelector('#contact-phone').value = ""
            this.form.querySelector('#contact-phone').parentNode.classList.remove('active')
            this.form.querySelector('label.phone').textContent = "Téléphone non valide"
            this.form.querySelector('label.phone').classList.add('error')
        }

        if (mail.match(/\S+@\S+\.\S+/)) {
            this.data.append("mail", mail)
            valid_inputs++
        } else {
            this.form.querySelector('#contact-mail').value = ""
            this.form.querySelector('#contact-mail').parentNode.classList.remove('active')
            this.form.querySelector('label.mail').textContent = "Email non valide"
            this.form.querySelector('label.mail').classList.add('error')
        }

        if (message.length > 0) {
            this.data.append("message", message)
            valid_inputs++
        } else {
            this.form.querySelector('label.message').textContent = "Message vide"
            this.form.querySelector('label.message').classList.add('error')
        }

        if (valid_inputs === 3) {
            this.form.querySelector('.submit').classList.add('disabled')
            progress.style.width = '50%';
            this.send()
        }

    }

    send(){
        let ajax = new XMLHttpRequest()

        // TODO: Switch this on prduction
        // ajax.open("POST", window.SETTINGS.contact_ajax_url, true)

        // USER DATA : this.userData

        ajax.open("GET", window.SETTINGS.contact_ajax_url, true)
        ajax.onload = () => {
          if (ajax.status == 200) {
            let resp = JSON.parse(ajax.responseText)
            if (resp.success === true) {
                this.form.querySelector('.progress').style.width = "100%"
                setTimeout(function () {
                  window.POPIN.hide('contact')
                  setTimeout(function () {
                    window.POPIN.display('thank_you')
                    setTimeout(function () {
                      window.POPIN.hide('thank_you')
                    }, 2000)
                  }, 800)
                }, 500)
            } else {
              alert("Erreur envoi de formulaire : réponse serveur on valide")
              this.form.querySelector('.progress').style.width = "0"
            }
          } else {
            alert("Erreur envoi de formulaire :", ajax.status)
            this.form.querySelector('.progress').style.width = "0"
          }
        }

        ajax.send(this.data)
    }
}
export default Contact_form
