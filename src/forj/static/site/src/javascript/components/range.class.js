import Draggable from "gsap/Draggable";
import * as TweenMax from "gsap";
import normalizeWheel from "normalize-wheel";

class Range {
  constructor() {
    this.presets = document.querySelectorAll(
      "section.module .presets-selector"
    );
    this.custom = document.querySelector("section.module .custom-selector");
    this.ranges = document.querySelectorAll("section.module .cursor-container");
    this.depth = 80;
    this.width = 140;
    this.height = 74;

    this.price = 0;
    this.tween_price = null;
    this.basket = null;
    this.need_roll = false;
    this.allready_scrolled = false;

    window.STORAGE.CURSOR = this;
  }

  init() {
    this.init_presets();
    this.init_ranges();
    window.STORAGE.TABLE.change_size(this.width, this.depth, this.height);
    this.update_range();
    this.init_bancs();
    this.update_price();
    this.init_scroll();
    this.init_roll_down();
  }

  init_roll_down() {
    let list = document.querySelector(".presets");
    let button = document.querySelector(".presets .mobile-dropdown");
    let shifter = document.querySelector(".shifter");

    let items = [...list.querySelectorAll("li")];
    let height = (items.length + 1) * items[0].offsetHeight;
    let elementHeight = items[0].offsetHeight;

    let expanded = false;

    let check_size = () => {
      if (window.innerWidth < 1180) {
        this.need_roll = true;
      } else {
        this.need_roll = false;
        expanded = false;
        shifter.style.transform = "translate(0,0)";
        shifter.style.webkitTransform = "translate(0,0)";
      }
    };
    check_size();

    window.addEventListener("resize", () => {
      //   console.log('YO');

      check_size();
    });

    button.addEventListener("click", () => {
      shifter.style.transform = "translate(0,0)";
      console.log(expanded);

      if (!expanded) {
        list.style.height = height + "px";
        expanded = true;
      } else {
        list.style.height = "50px";
        expanded = false;
      }
    });

    let that = this;
    for (var i = 0; i < items.length; i++) {
      items[i].addEventListener("click", function() {
        if (that.need_roll) {
          list.style.height = "50px";
          expanded = false;
          let offset = items.indexOf(this) * -64;
          shifter.style.transform = "translate(0," + offset + "px)";
          shifter.style.webkitTransform = "translate(0," + offset + "px)";
        }
      });
    }
  }

  init_scroll() {
    let that = this;
    function scroll() {
      if (!that.allready_scrolled) {
        document.body.classList.remove("fixed");
        setTimeout(function() {
          GL.anim_in();
        }, 500);
      }

      let module = document.querySelector(".module");
      let distance = module.getBoundingClientRect().top;

      let tmp = { value: window.scrollY };

      TweenMax.to(tmp, 1, {
        value: distance,
        ease: Expo.easeInOut,
        onStart: function() {
          // document.querySelector('.mobile-nav').classList.add('hidden')
        },
        onUpdate: function() {
          window.scrollTo(0, this.target.value);
        },
        onComplete: () => {
          that.allready_scrolled = true;
          //   document.querySelector('header').style.display = 'none'
          //   document.querySelector('nav').style.display = 'none'
          //   document.querySelector('.mobile-nav').classList.add('dark')
        }
      });
    }

    let scroll_links = document.querySelectorAll(".scroll-to");
    for (var i = 0; i < scroll_links.length; i++) {
      scroll_links[i].addEventListener("click", function() {
        scroll();
      });
    }

    let wheel_fired = false;
    let prevent = true;
    window.addEventListener("mousewheel", e => {
      if (window.scrollY > 10 && !this.allready_scrolled) {
        this.allready_scrolled = true;
        GL.anim_in();
        document.body.classList.remove("fixed");
        prevent = false;
        return;
      }
      if (prevent) {
        e.preventDefault();
        setTimeout(() => {
          prevent = false;
        }, 1000);
      }
      const normalized_wheel = normalizeWheel(e);
      let wheel = normalized_wheel.spinY;
      if (wheel > 0 && !this.allready_scrolled && !wheel_fired) {
        wheel_fired = true;
        scroll();
      }
    });

    //   document.querySelector('.slider').addEventListener('click', (e)=>{
    //       if (prevent) {
    //           e.preventDefault()
    //           setTimeout(() => {
    //               prevent = false
    //           }, 1000)
    //       }
    //       scroll()
    //   })
  }

  init_presets() {
    let that = this;
    for (var i = 0; i < this.presets.length; i++) {
      this.presets[i].addEventListener("click", function() {
        let depth = this.dataset.depth;
        let width = this.dataset.width;
        let height = this.dataset.height;
        let bancs_selector = document.querySelector("section.module .bancs");
        let banc_enabled = document.querySelector(
          "section.module .banc-enabled"
        );

        if (this === banc_enabled) {
          bancs_selector.classList.add("active");
        } else {
          bancs_selector.classList.remove("active");
        }

        window.STORAGE.TABLE.change_size(width, depth, height);
        setTimeout(() => {
          if (window.innerWidth < 960) {
            window.GL.mouse.z = -0.5;
          } else {
            window.GL.mouse.z = -0.2;
          }
        }, 470);

        that.depth = depth;
        that.width = width;
        that.height = height;
        that.update_range();
        that.update_bancs();

        for (var i = 0; i < that.presets.length; i++) {
          that.presets[i].classList.remove("selected");
          that.presets[i].classList.add("active");
        }
        that.custom.classList.remove("selected");
        this.classList.add("selected");

        window.GL.remove_bancs();
      });
    }
  }

  init_ranges() {
    this.draggables = [];
    for (var i = 0; i < this.ranges.length; i++) {
      let range = this.ranges[i];
      let cursor = range.querySelector(".cursor");
      let min = JSON.parse(range.dataset.min);
      let max = JSON.parse(range.dataset.max);
      let type = range.dataset.type;
      let bancs_selector = document.querySelector("section.module .bancs");
      let draggable = Draggable.create(cursor, {
        type: "x",
        bounds: range,
        onDrag: () => {
          let ratio = draggable[0].x / draggable[0].maxX;
          let size = Math.round(min + (max - min) * ratio);
          range.parentNode.querySelector(".value").textContent = size;

          if (type === "depth") {
            this.depth = size;
          } else if (type === "width") {
            this.width = size;
          } else if (type === "height") {
            this.height = size;
          }
          window.STORAGE.TABLE.change_size(this.width, this.depth, this.height);
          for (var i = 0; i < window.GL.bancs.length; i++) {
            window.GL.bancs[i].change_size(this.width - 25, 32, 45);
          }

          if (type === "height") {
            GL.remove_bancs();
            this.update_bancs();
            bancs_selector.classList.remove("active");

            for (var i = 0; i < this.presets.length; i++) {
              this.presets[i].classList.remove("selected");
              this.presets[i].classList.remove("active");
            }
            this.custom.classList.add("selected");
          }
        },
        onRelease: () => {}
      });
      this.draggables.push(draggable[0]);
    }
  }

  update_bancs() {
    let banc_count = document.querySelector(".banc-count");
    let add_banc = document.querySelector(".add-banc");
    let remove_banc = document.querySelector(".remove-banc");

    add_banc.classList.remove("disabled");
    remove_banc.classList.remove("disabled");

    if (window.GL.bancs.length === 2) {
      add_banc.classList.add("disabled");
    }
    if (window.GL.bancs.length === 0) {
      remove_banc.classList.add("disabled");
    }
  }

  init_bancs() {
    let banc_count = document.querySelector(".banc-count");
    let add_banc = document.querySelector(".add-banc");
    let remove_banc = document.querySelector(".remove-banc");

    add_banc.addEventListener("click", () => {
      let count = JSON.parse(banc_count.textContent);
      if (window.GL.bancs.length < 2) {
        window.GL.add_banc();
        this.update_price();
        count++;
        banc_count.textContent = count;
        if (window.GL.bancs.length === 2) {
          add_banc.classList.add("disabled");
        } else {
          add_banc.classList.remove("disabled");
          remove_banc.classList.remove("disabled");
        }
      }
    });
    remove_banc.addEventListener("click", () => {
      let count = JSON.parse(banc_count.textContent);
      if (window.GL.bancs.length > 0) {
        window.GL.remove_banc();
        this.update_price();
        count--;
        banc_count.textContent = count;
        if (window.GL.bancs.length === 0) {
          remove_banc.classList.add("disabled");
        } else {
          add_banc.classList.remove("disabled");
          remove_banc.classList.remove("disabled");
        }
      }
    });
  }

  update_price() {
    let surface =
      window.STORAGE.TABLE.width * window.STORAGE.TABLE.depth / 40000;
    surface = Math.max(surface, 1);

    let plateau_price;
    if (window.STORAGE.TABLE.active_desk === "none") {
      plateau_price = window.SETTINGS.prices.sans_plateau;
    } else if (window.STORAGE.TABLE.active_desk === "chene") {
      plateau_price = window.SETTINGS.prices.chene_plateau;
    } else if (window.STORAGE.TABLE.active_desk === "metal") {
      plateau_price = window.SETTINGS.prices.metal;
    } else {
      plateau_price = window.SETTINGS.prices.douglas;
    }

    let laquage = 0;
    if (window.STORAGE.TABLE.outside) {
      laquage = window.SETTINGS.prices.traitement_exterieur;
    }

    let prices = {
      time: window.SETTINGS.prices.main_d_oeuvre,
      plateau: plateau_price,
      vernis: window.SETTINGS.prices.vernis,
      acier: window.SETTINGS.prices.acier,
      laquage: laquage
    };

    //   let plop = {
    //       sans_plateau : 0,
    //       chene_plateau : 133,
    //       douglas : 60,
    //       metal: 60,
    //       traitement_exterieur: 250,
    //       main_d_oeuvre : 104,
    //       vernis : 15,
    //       acier : 40
    //   }

    let total = 42;
    for (let key in prices) {
      if (!prices.hasOwnProperty(key)) continue;
      prices[key] *= surface;
      total += prices[key];
    }

    // Marge
    total *= 1.5;
    // TVA
    total *= 1.2;
    total = Math.ceil(total);

    for (var i = 0; i < window.GL.bancs.length; i++) {
      total += 250;
    }

    this.price = total;

    let diplayed_price = {};
    diplayed_price.dom = document.querySelector("#price-value");
    diplayed_price.value = parseFloat(diplayed_price.dom.textContent).toFixed(
      2
    );

    this.tween_price = TweenMax.to(diplayed_price, 1, {
      value: total,
      ease: Expo.easeInOut,
      onUpdate: () => {
        if (this.tween_price.target.value.toFixed) {
          diplayed_price.dom.textContent = this.tween_price.target.value.toFixed(
            2
          );
        }
      }
    });

    this.update_labels();
  }

  update_labels() {
    let infos = [
      {
        depth: document.querySelector("section.infos .depth"),
        width: document.querySelector("section.infos .width"),
        height: document.querySelector("section.infos .height"),
        active_desk: document.querySelector("section.infos .desk"),
        active_color: document.querySelector("section.infos .color")
      },
      {
        depth: document.querySelector(".basket .depth"),
        width: document.querySelector(".basket .width"),
        height: document.querySelector(".basket .height"),
        active_desk: document.querySelector(".basket .desk"),
        active_color: document.querySelector(".basket .color")
      }
    ];

    for (var i = 0; i < infos.length; i++) {
      for (let key in infos[i]) {
        if (!infos[i].hasOwnProperty(key)) continue;
        if (key === "depth" || key === "width" || key === "height") {
          infos[i][key].textContent = window.STORAGE.TABLE[key] / 2 + ",00";
        } else {
          infos[i][key].textContent = window.STORAGE.TABLE[key];
        }
      }
    }

    let outside = document.querySelector("section.infos .outside");
    if (window.STORAGE.TABLE.outside) {
      outside.innerHTML = "<br>Traitement extérieur";
    } else {
      outside.textContent = "";
    }

    let bancs = document.querySelector("section.infos .bancs");
    if (window.GL.bancs.length > 0) {
      bancs.textContent = "(" + window.GL.bancs.length + ")";
    } else {
      bancs.textContent = "(0)";
    }

    let outside_popin = document.querySelector(".basket .outside");
    if (window.STORAGE.TABLE.outside) {
      outside_popin.innerHTML = "<br>Traitement extérieur";
    } else {
      outside_popin.textContent = "";
    }

    let bancs_popin = document.querySelector(".basket .bancs");
    if (window.GL.bancs.length > 0) {
      bancs_popin.textContent = "(" + window.GL.bancs.length + ")";
    } else {
      bancs_popin.textContent = "(0)";
    }

    this.update_selection();
  }

  update_selection() {
    this.basket = {
      depth: window.STORAGE.TABLE.depth / 2,
      width: window.STORAGE.TABLE.width / 2,
      height: window.STORAGE.TABLE.height / 2,
      desk: window.STORAGE.TABLE.active_desk,
      color: window.STORAGE.TABLE.active_color,
      bancs: window.GL.bancs.length,
      outside: window.STORAGE.TABLE.outside,
      price: this.price
    };
  }

  update_range() {
    let ranges = [];
    for (var i = 0; i < this.ranges.length; i++) {
      let range = this.ranges[i];
      ranges.push({
        min: JSON.parse(range.dataset.min),
        max: JSON.parse(range.dataset.max),
        type: range.dataset.type,
        cursor: range.querySelector(".cursor"),
        value: range.parentNode.querySelector(".value")
      });
    }

    this.depth = Math.min(Math.max(this.depth, ranges[0].min), ranges[0].max);
    this.width = Math.min(Math.max(this.width, ranges[1].min), ranges[1].max);
    this.height = Math.min(Math.max(this.height, ranges[2].min), ranges[2].max);

    let depth_ratio =
      (this.depth - ranges[0].min) / (ranges[0].max - ranges[0].min);
    let width_ratio =
      (this.width - ranges[1].min) / (ranges[1].max - ranges[1].min);
    let height_ratio =
      (this.height - ranges[2].min) / (ranges[2].max - ranges[2].min);

    let depth_pixel = Math.round(this.draggables[0].maxX * depth_ratio);
    let width_pixel = Math.round(this.draggables[1].maxX * width_ratio);
    let height_pixel = Math.round(this.draggables[2].maxX * height_ratio);

    TweenMax.to(ranges[0].cursor, 1, { x: depth_pixel, ease: Expo.easeInOut });
    TweenMax.to(ranges[1].cursor, 1, { x: width_pixel, ease: Expo.easeInOut });
    TweenMax.to(ranges[2].cursor, 1, { x: height_pixel, ease: Expo.easeInOut });

    let values = {
      depth: JSON.parse(ranges[0].value.textContent),
      width: JSON.parse(ranges[1].value.textContent),
      height: JSON.parse(ranges[2].value.textContent)
    };

    TweenMax.to(values, 1, {
      depth: this.depth,
      width: this.width,
      height: this.height,
      onUpdate: function() {
        ranges[0].value.textContent = Math.round(this.target.depth);
        ranges[1].value.textContent = Math.round(this.target.width);
        ranges[2].value.textContent = Math.round(this.target.height);
      }
    });
  }
}
export default Range;
