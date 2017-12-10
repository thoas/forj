const mobileNav = document.querySelector('nav')
const hamburger = document.querySelector('.hamburger')

hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('active')
  mobileNav.classList.toggle('active')
})
