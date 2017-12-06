import * as TOOLS from "./components/tools.class";
import THREE_Controller from "./components/THREE_Controller.class";
import Range from "./components/range.class";
import Sticky_bar from "./components/sticky_bar.class";
import Slider from "./components/slider.class";
import Basket from "./components/basket.class";
import Collection_Carroussel from "./components/collection_carroussel";
import Popins from './components/popins.stuff'


let three = {};
if (document.body.classList.contains("main")) {
  three = new THREE_Controller({ container: document.querySelector(".webgl") });
  let range = new Range();
  let sticky = new Sticky_bar(document.querySelector("section.infos"));
  new Popins(["more_color", "gallery"])
} else if (document.body.classList.contains("collection")) {
  new Collection_Carroussel();
}

let sliders = document.querySelectorAll(".slider");
for (var i = 0; i < sliders.length; i++) {
  let carroussel = new Slider(sliders[i]);
}

let hamburger = document.querySelector(".hamburger");
let nav_mobile = document.querySelector("nav");

hamburger.addEventListener("click", () => {
  hamburger.classList.toggle("active");
  nav_mobile.classList.toggle("active");
});

new Basket();

animate();

function animate() {
  requestAnimationFrame(animate);

  // Updating components
  if (three.renderer != undefined) {
    three.update();
  }
}
