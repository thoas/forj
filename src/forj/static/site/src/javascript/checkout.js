document.addEventListener("DOMContentLoaded", e => {
  const diff = document.querySelector('#diff');
  const billingWrapper = document.querySelector('#billing-wrapper');

  diff.addEventListener('change', e => {
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
});
