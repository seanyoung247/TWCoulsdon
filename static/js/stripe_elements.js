
/*
 * Interacts with stripe for secure payments
 *
 * Largely based on the boutique-ado project example
 *
 * Core logic/payment flow for this comes from here:
 *    https://stripe.com/docs/payments/accept-a-payment
 *
 * CSS from here:
 *    https://stripe.com/docs/stripe-js
 */

const stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
const clientSecret = $('#id_client_secret').text().slice(1, -1);
const stripe = Stripe(stripePublicKey);
const elements = stripe.elements();

const style = {
  base: {
    color: '#14161A',
    fontFamily: '"Roboto", sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#EBEDF0'
    }
  },
  invalid: {
    color: '#dc3545',
    iconColor: '#dc3545'
  }
};

const card = elements.create('card', {style: style});
card.mount('#card-element');


function displayCardError(message) {
  const errorDiv = $('#card-errors');
  errorDiv.html(`<span>${message}</span>`);
}
function clearCardError() {
  const errorDiv = $('#card-errors');
  errorDiv.text('');
}

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
  if (event.error)
    displayCardError(event.error.message);
  else
    clearCardError();
});

// Form submission
$( '#payment-form' ).submit( function(e) {
  e.preventDefault();

  // Disable input elements to prevent multiple submissions
  card.update({ 'disabled':true });
  $( '#submit-button' ).prop('disabled', true);

  // Show the loading overlay
  $( '#loading-overlay' ).fadeToggle(100);

  // Prepare the pre-checkout data to send to the server
  const saveToProfile = $( '#id-save-info' ).prop('checked');
  const postData = {
    'csrfmiddlewaretoken': csrfToken,
    'save_to_profile': saveToProfile,
    'client_secret': clientSecret,
  };
  const url = '/boxoffice/checkout/cache_data/'

  // Post the pre-checkout data
  $.post(url, postData).done(function() {

    // Check user payment
    stripe.confirmCardPayment(clientSecret, {
      payment_method: {
        card: card,
        billing_details: {
          name: $.trim(form.full_name.value),
          phone: $.trim(form.phone_number.value),
          email: $.trim(form.email.value),
        }
      }
    // Payment check returned
    }).then(function(result) {
      if (result.error) {
        displayCardError(result.error.message);
        //
        $('#loading-overlay').fadeToggle(100);
        card.update({ 'disabled': false});
        $('#submit-button').attr('disabled', false);
      } else {
        if (result.paymentIntent.status === 'succeeded') {
          // If the user has paid post the form to the checkout
          $( '#payment-form' ).submit();
        }
      }
    });

  // Posting pre-checkout failed
  }).fail(function() {
    // Messaging is not yet implimented, will need to do that...
    location.reload();
  });
});
