class Collection_Carroussel {
    constructor(options){

        this.target = document.querySelectorAll('.carroussel')
        this.sliders = []

        for (var i = 0; i < this.target.length; i++) {
            this.init(this.target[i])
        }

    }

    init(el){        
        let arrow_right = el.querySelector('.arrow.right')
        let arrow_left = el.querySelector('.arrow.left')
        let lis = el.querySelectorAll('li')
        let that = this
        let pause = false

        let active_element = 0 
        this.reset_lis(el)
        lis[0].classList.add('active')

        let timer = setTimeout(function () {}, 0)

        function onRight(evt){
            that.reset_lis(el)
            active_element >= lis.length - 1 ? active_element = 0 : active_element++ 
            lis[active_element].classList.add('active')
            if (evt != undefined) {return}
            pause = true
            clearTimeout(timer)
            timer = setTimeout(function(){pause = false}, 5000)
        }

        function onLeft(evt){
            that.reset_lis(el)
            active_element <= 0 ? active_element = lis.length - 1 : active_element--
            lis[active_element].classList.add('active')
            if (evt != undefined) {return}
            pause = true
            clearTimeout(timer)
            timer = setTimeout(function(){pause = false}, 5000)
        }

        arrow_left.addEventListener('click', onLeft)
        arrow_right.addEventListener('click', onRight)


        setInterval(function(){
            if (!pause) {
                onRight()
            }
        }, 3000 + Math.round(Math.random() * 2000))


    }

    reset_lis(el){
        let lis = el.querySelectorAll('li')
        for (var i = 0; i < lis.length; i++) {
            var li = lis[i]
            li.classList.remove('active')
        }
    }
}
export default Collection_Carroussel