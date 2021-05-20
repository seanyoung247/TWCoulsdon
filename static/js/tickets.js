/*
 * Provides code for adding and removing tickets from the basket.
 */

// Shows the add tickets modal and requests event data from the server.
$( '.btn-add-tickets' ).click( function() {
  const modal = $('#add-ticket-modal');
  const url = `/boxoffice/buy_tickets/?event=${$( this ).data('event-id')}`

  // Set the modal title
  modal.find( '.modal-title' ).text( $( this ).data('event-title') )

  // Set the modal to it's preloaded state
  modal.find( '#add-tickets-form-wrapper' ).html("<h5>Loading...</h5>");
  modal.find( '#add-tickets-list' ).html("");
  modal.find( '#add-tickets-total' ).text("0.00");

  // Request modal HTML from server
  $.get( url, function(data) {
    const formWrapper = $('#add-tickets-form-wrapper');
    if (data.form) {
      formWrapper.html(data.form);
      // Don't let the user select more tickets than there are
      $( '#add-ticket-quantity' ).attr(
        'max', $( '#add-ticket-date' ).find( ':selected' ).data('tickets-left'));
    }
  });

  modal.modal({
    backdrop: modal.data('backdrop'),
    keyboard: modal.data('keyboard')
  });
});

// Date checks
$( '#add-tickets-form-wrapper' ).on( 'change', '#add-ticket-date', function(e) {
  // Set the maximum quantity to be the number of tickets left
  $( '#add-ticket-quantity' ).attr(
    'max', $( '#add-ticket-date' ).find( ':selected' ).data('tickets-left'));
});

/*
 * Spinner controls for the number field
 */
function spinnerBtn(target, step) {
  const min = parseInt(target.attr('min'));
  const max = parseInt(target.attr('max'));
  let value = parseInt(target.val()) + step

  if (value >= min && value <= max) target.val( value );
}

$( '#add-tickets-form-wrapper' ).on( 'click', 'button.btn-dec', function(e) {
  e.preventDefault();
  spinnerBtn($( $( this ).data('target') ), -1);
});

$( '#add-tickets-form-wrapper' ).on( 'click', 'button.btn-inc', function(e) {
  e.preventDefault();
  spinnerBtn($( $( this ).data('target') ), 1);
});

// Prevents the quantity value going out of bounds
$( '#add-tickets-form-wrapper' ).on( 'change', '#add-ticket-quantity', function(e) {
  const current = $( this );
  const min = parseInt(current.attr('min'));
  const max = parseInt(current.attr('max'));

  if (current.val() > max) current.val(max);
  if (current.val() < min) current.val(min);
});
// Add ticket button

// Add to basket button