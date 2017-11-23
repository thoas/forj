import * as axios from 'axios'

document.addEventListener("DOMContentLoaded", e => {
  const billingWrapper = document.querySelector('#billing-wrapper');

  document.querySelector('#diff').addEventListener('change', e => {
    if (e.target.checked) {
      billingWrapper.style.display = "block";
    } else {
      billingWrapper.style.display = "none";
    }
  })

  const addressTypeChange = (radios, typeInput) => {
    radios.forEach(radio => {
      radio.addEventListener('change', e => {
        if (radio.value == 1) {
          typeInput.style.display = 'none';
        } else {
          typeInput.style.display = 'block';
        }
      });
    });
  }

  addressTypeChange(
    document.querySelectorAll('input[name=shipping-address-type]'),
    document.querySelector('#id_shipping-address-business_name')
  );

  addressTypeChange(
    document.querySelectorAll('input[name=billing-address-type]'),
    document.querySelector('#id_billing-address-business_name')
  );

  document.querySelector('input[name=shipping-address-type]:checked').dispatchEvent(new Event('change'));
  document.querySelector('input[name=billing-address-type]:checked').dispatchEvent(new Event('change'));

  const cartContainer = document.querySelector('.basket-container');
  const totalContainer = document.querySelector('#total-container');

  axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
  axios.defaults.headers.post['X-Requested-With'] = 'XMLHttpRequest';

  document.querySelectorAll('.article-container p.delete a').forEach(elem => {
    elem.addEventListener('click', e => {
      e.preventDefault();

      const current = e.target;
      const articleContainer = current.parentNode.parentNode.parentNode;

      var params = new URLSearchParams();
      params.append('action', current.getAttribute('data-action'));
      params.append('reference', current.getAttribute('data-reference'));

      axios.post(current.getAttribute('href'), params).then(res => {
        cartContainer.removeChild(articleContainer);
        totalContainer.innerHTML = res.data.total_formatted;
      })
    })
  })
});
