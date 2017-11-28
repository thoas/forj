Stripe.setPublishableKey(window.FJ.stripe_publishable_key);

const paymentForm = document.getElementById('payment-form');
const cardNumber = document.getElementById('id_number');
const cardCvc = document.getElementById('id_cvc');
const expireYear = document.getElementById('id_expire_year');
const expireMonth = document.getElementById('id_expire_month');
const token = document.getElementById('id_token');
const expireWrapper = document.getElementById('expiry-wrapper');

[expireYear, expireMonth].forEach(elem => {
  elem.addEventListener('change', e => {
    elem.previousElementSibling.textContent = elem.value;
  });
});

paymentForm.addEventListener('submit', e => {
  if (paymentForm.classList.contains('processing')) {
    return;
  }

  e.preventDefault();

  let hasErrors = false;

  if (!Stripe.card.validateCardNumber(cardNumber.value)) {
    cardNumber.parentNode.classList.add('error');
    hasErrors = true;
  } else {
    cardNumber.parentNode.classList.remove('error');
  }

  if (!Stripe.card.validateCVC(cardCvc.value)) {
    cardCvc.parentNode.classList.add('error');
    hasErrors = true;
  } else {
    cardCvc.parentNode.classList.remove('error');
  }

  var month = parseInt(expireMonth.value, 10);
  if (month < 10) {
    month = '0' + month;
  }

  if (!Stripe.card.validateExpiry(month, expireYear.value)) {
    expireWrapper.classList.add('error');
    hasErrors = true;
  } else {
    expireWrapper.classList.remove('error');
  }

  if (hasErrors) {
    return;
  }

  var cardData = {
    number: cardNumber.value,
    exp_month: month,
    exp_year: expireYear.value.substr(2),
    cvc: cardCvc.value
  };

  paymentForm.classList.add('processing');

  Stripe.source.create({
    type: 'card',
    card: cardData
  }, (status, response) => {
    token.value = response.id;
    paymentForm.submit();
  });
});
