class Basket {

    constructor() {

        this.check_basket()
        this.init()
        if (document.body.classList.contains('main')) {
          this.init_event()
        }

        window.STORAGE.basket = this

    }

    init(){
        if (this.items === null) {
            this.set_basket([])
        } else {
            // console.log('allready in basket :', this.items);
            if (document.querySelector('#items-numbers')) {
                document.querySelector('#items-numbers').innerHTML = this.items.length
                document.querySelector('.basket-icon').innerHTML = "<span>(" + this.items.length + ")</span>"
            }
        }
    }

    init_event(){
        let launcher = document.querySelector('#add-to-basket')
        launcher.addEventListener('click', (e)=>{
            e.preventDefault()
            this.add_current_to_basket()
            window.POPIN.display('basket')
        })
    }

    add_current_to_basket(){
        let item = JSON.parse(JSON.stringify(STORAGE.CURSOR.basket))
        this.items.push(item)
        this.set_basket(this.items)
    }

    remove_from_basket(index){
        this.items.splice(index, 1)
        this.set_basket(this.items)
    }

    check_basket(){
        this.items = JSON.parse(localStorage.getItem("forj_basket"))
        window.BASKET = this.items
    }

    set_basket(items){
        localStorage.setItem("forj_basket", JSON.stringify(items))
        this.check_basket()
    }
}
export default Basket
