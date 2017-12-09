class Popins {
  constructor(list) {
    this.background = document.querySelector(".popin-background");
    this.activated = list;

    for (var i = 0; i < this.activated.length; i++) {
      this[this.activated[i]]();
    }

    this.active_popin = null;

    window.POPIN = this;

    this.init_event_background();
  }

  init_event_background() {
    this.background.addEventListener("click", () => {
      if (this.active_popin !== null) {
        this.hide(this.active_popin);
      }
    });
  }

  display(name) {
    this.background.classList.add("active");
    this["popin_" + name].classList.remove("hidden");
    setTimeout(() => {
      this["popin_" + name].classList.add("active");
    }, 10);
    this.active_popin = name;
  }

  basket() {
    let popin_basket = document.querySelector(".popin.basket");
    this.popin_basket = popin_basket;

    popin_basket.querySelector(".return").addEventListener("click", e => {
      this.hide("basket");
    });
  }

  hide(name) {
    this["popin_" + name].classList.remove("active");
    setTimeout(() => {
      this["popin_" + name].classList.add("hidden");
      this.background.classList.remove("active");
      this.active_popin = null;
    }, 500);
  }

  more_color() {
    let popin_more_color = document.querySelector(".more");
    let more_color_open = false;

    popin_more_color.addEventListener("click", function() {
      setTimeout(() => {
        if (more_color_open) {
          this.classList.remove("active");
          more_color_open = false;
        } else {
          this.classList.add("active");
          more_color_open = true;
        }
      }, 10);
    });
    document
      .querySelector("section.module .params")
      .addEventListener("click", function() {
        if (more_color_open) {
          popin_more_color.classList.remove("active");
          setTimeout(() => {
            more_color_open = false;
          }, 20);
        }
      });
  }

  gallery() {
    let gallery_launcher = document.querySelector(".gallery-launcher");
    let gallery = document.querySelector("section.gallery");
    let gallery_right = document.querySelector("section.gallery .right");
    let gallery_left = document.querySelector("section.gallery .left");
    let active_gallery_index = 0;

    gallery_launcher.addEventListener("click", function() {
      gallery.classList.add("active");
    });
    let photos_gallery = document.querySelectorAll("section.gallery li");
    for (var i = 0; i < photos_gallery.length; i++) {
      photos_gallery[i].classList.remove("active");
    }
    photos_gallery[active_gallery_index].classList.add("active");

    gallery_right.addEventListener("click", function() {
      for (var i = 0; i < photos_gallery.length; i++) {
        photos_gallery[i].classList.remove("active");
      }
      if (active_gallery_index < photos_gallery.length - 1) {
        active_gallery_index++;
      } else {
        active_gallery_index = 0;
      }
      photos_gallery[active_gallery_index].classList.add("active");
    });

    gallery_left.addEventListener("click", function() {
      for (var i = 0; i < photos_gallery.length; i++) {
        photos_gallery[i].classList.remove("active");
      }
      if (active_gallery_index > 0) {
        active_gallery_index--;
      } else {
        active_gallery_index = photos_gallery.length - 1;
      }
      photos_gallery[active_gallery_index].classList.add("active");
    });

    gallery.querySelector(".background").addEventListener(
      "click",
      function() {
        gallery.classList.remove("active");
      },
      false
    );
  }
}
export default Popins;
