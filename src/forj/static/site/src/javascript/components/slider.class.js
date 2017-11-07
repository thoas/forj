class Slider {

    constructor(target) {
        this.target = target
        this.current_index = 0
        this.texts = this.target.querySelectorAll('.text-slider')
        this.covers = this.target.querySelectorAll('.cover')
        this.progress = this.target.querySelector('.progress')

        this.init_events()

        setTimeout( ()=>{
          this.progress.classList.add('active')
        }, 100)
    }

    init_events(){
        this.right_button = this.target.querySelector('.right')
        this.left_button = this.target.querySelector('.left')

        this.right_button.addEventListener('click', ()=>{
            this.on_click('right')
        })
        this.left_button.addEventListener('click', ()=>{
            this.on_click('left')
        })
        this.progress.addEventListener('transitionend', ()=>{
            this.on_click('right')
        })
    }

    on_click(dir){
        for (var i = 0; i < this.texts.length; i++) {
          this.texts[i].classList.remove('active')
        }
        for (var i = 0; i < this.covers.length; i++) {
          this.covers[i].classList.remove('active')
        }

        if (dir === 'right') {
            this.current_index ++
            if (this.current_index > this.texts.length - 1) { this.current_index = 0 }
            this.texts[this.current_index].classList.add('active')
            this.covers[this.current_index].classList.add('active')
        } else {
            this.current_index --
            if (this.current_index < 0) { this.current_index = this.texts.length - 1 }
            this.texts[this.current_index].classList.add('active')
            this.covers[this.current_index].classList.add('active')
        }

        this.progress.classList.remove('active')
        setTimeout( ()=>{
          this.progress.classList.add('active')
        }, 100)

    }

}
export default Slider
