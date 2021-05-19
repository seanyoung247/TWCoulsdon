/*
 * Provides code for adding and removing tickets from the basket.
 */

// Shows the add tickets modal and requests event data from the server.
$( '.btn-add-tickets' ).click( function() {
  const modal = $('#add-ticket-modal');

  // Set the modal title
  modal.find( '.modal-title' ).text( $( this ).data('event-title') )

  // Set the modal to it's preloaded state
  modal.find( '#add-tickets-form-wrapper' ).html("<h5>Loading...</h5>");
  modal.find( '#add-tickets-ticket-list' ).html("");

  // Request modal HTML from server
  $.get( `/boxoffice/buy_tickets/?event=${$( this ).data('event-id')}`, function(data) {
    const formWrapper = $('#add-tickets-form-wrapper');
    if (data.form) formWrapper.html(data.form);
  });

  modal.modal({
    backdrop: modal.data('backdrop'),
    keyboard: modal.data('keyboard')
  });
});

// Spinner controls for the number field

// Add ticket button

// Add to basket button