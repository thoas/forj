import * as TOOLS from "./components/tools";
import THREEController from "./components/THREEController";
import Range from "./components/Range";
import StickyBar from "./components/StickyBar";
import Slider from "./components/Slider";
import CollectionCarousel from "./components/CollectionCarousel";
import Popins from './components/Popins'


let three = {};
if (document.body.classList.contains("main")) {
  three = new THREEController({ container: document.querySelector(".webgl") });
  let range = new Range();
  let sticky = new StickyBar(document.querySelector("section.infos"));
  new Popins(["more_color", "gallery", "basket"])

  document.querySelector("#add-to-basket").addEventListener("click", e => {
    e.preventDefault();
    window.POPIN.display("basket");
  });
} else if (document.body.classList.contains("collection")) {
  new CollectionCarrousel();
}

document.querySelectorAll(".slider").forEach(node => {
  new Slider(node);
})

let hamburger = document.querySelector(".hamburger");
let nav_mobile = document.querySelector("nav");

hamburger.addEventListener("click", () => {
  hamburger.classList.toggle("active");
  nav_mobile.classList.toggle("active");
});

const animate = () => {
  requestAnimationFrame(animate);

  // Updating components
  if (three.renderer != undefined) {
    three.update();
  }
}

animate();
