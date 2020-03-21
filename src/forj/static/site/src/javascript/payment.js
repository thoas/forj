setTimeout(() => {
  const stripe = Stripe(window.FJ.stripe_publishable_key)

  stripe
    .redirectToCheckout({
      sessionId: window.FJ.stripe_session_id
    })
    .then(function(result) {})
}, 2000)
