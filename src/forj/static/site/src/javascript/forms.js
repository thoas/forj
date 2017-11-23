document.addEventListener("DOMContentLoaded", e => {
  const wrappers = document.querySelectorAll('.input-wrapper');

  wrappers.forEach(elem => {
    elem.addEventListener('change', () => {
      setTimeout(() => {
        wrappers.forEach(child => {
          const input = child.querySelector('input');

          if (input) {
            if (input.value.length > 0) {
              child.classList.add('filled')
              child.classList.add('active')
            } else {
              child.classList.remove('filled')
            }
          }
        })
      }, 100)
    })

    elem.addEventListener('focusin', (e) => {
      elem.classList.add('active')
    });

    elem.addEventListener('focusout', (e) => {
      if (elem.querySelector('input')) {
        if (elem.querySelector('input').value.length === 0) {
          elem.classList.remove('active');
        } else {
          elem.classList.add('filled');
        }
      }
    });
  });
});
