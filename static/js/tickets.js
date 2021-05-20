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

// Updates available tickets - Only reflects the local user's actions
function updateAvailableTickets(date, adjustment) {
  // Get the date option to update
  const dateOption = $( `#add-ticket-date > option[value="${date}"]` );
  const newCount = parseInt(dateOption.data('tickets-left')) + adjustment

  // Are there any tickets left after these?
  if (newCount > 0) {
    // Set the ticket count to the new value
    dateOption.data('tickets-left', newCount);
    // Make sure the option is selectable
    dateOption.prop('disabled', false);
  } else {
    dateOption.data('tickets-left', 0);
    // Option should be disabled
    dateOption.prop('disabled', true);
  }

  // Is the updated date the same as the currently selected date?
  if ( dateOption[0] == $( '#add-ticket-date' ).find( ':selected' )[0] ) {
    if (dateOption.prop('disabled')) $( '#add-ticket-date' ).val("");
    else $( '#add-ticket-quantity' ).attr('max', newCount);
  }
}

// Updates visual price
function updateTotalPrice() {
  const list = $( '#add-tickets-list' );
  let total = 0;

  // Traverse the list, getting the price and quantity of each item
  list.children('.add-ticket-list-item').each(function() {
    total += parseFloat( $( this ).data('price') ) * parseInt( $( this ).data('quantity') );
  });

  // Display the new total
  $( '#add-tickets-total' ).text(total.toFixed(2));
}

// Add ticket button
$( '#add-tickets-form-wrapper' ).on( 'click', '#add-ticket-submit', function(e) {
  e.preventDefault();

  // Get the ticket order information
  // Event date information
  const date = $( '#add-ticket-date' ).find( ':selected' );

  if (date.val() != null) {
    // Ticket type information
    const ticket = $( '#add-ticket-type' ).find( ':selected' );
    const unitPrice = parseFloat(ticket.data('unit-price'));

    const qtyInput = $( '#add-ticket-quantity' );
    const adjustment = parseInt(qtyInput.val());
    let quantity = adjustment;
    let subTotal = (unitPrice * quantity).toFixed(2);

    // Reset the quantity value, it's no longer needed
    qtyInput.val(qtyInput.attr('min'));

    // Is there already a ticket line of this type and date?
    let listItem = $(`#${date.val()}-${ticket.val()}`);
    if (listItem.length > 0) {
      // Add to the existing line
      quantity += listItem.data('quantity');
      subTotal = unitPrice * quantity;

      listItem.data('quantity', quantity);
      listItem.data('price', unitPrice);

      listItem.children('.item-quantity').text(quantity);
      listItem.children('.item-subTotal').text(`£${subTotal.toFixed(2)}`);
    } else {
      // Create a new line
      // Construct the visual element
      listItem = $(
        `<li id="${date.val()}-${ticket.val()}" class="add-ticket-list-item form-row">
          <div class="col-12 col-lg-4">${date.text()}</div>
          <div class="col-12 col-lg-4">${ticket.text()}</div>
          <div class="item-quantity col-9 col-lg-2">${quantity}</div>
          <div class="item-subTotal col-3 col-lg-2">£${subTotal}</div>

          <button type="button" class="delete-list-item close" aria-label="Delete">
            <span aria-hidden="true">&times;</span>
          </button>
        </li>`
      );
    }

    // Append the list item
    $( '#add-tickets-list' ).append(listItem);

    // Add the data attributes
    listItem.data('date-id', date.val());     //EventDate.id
    listItem.data('ticket-id', ticket.val()); //TicketType.id
    listItem.data('quantity', quantity);      //Ticket quantity
    listItem.data('price', unitPrice);        //Ticket Unit price

    // Update available tickets
    updateAvailableTickets(date.val(), (adjustment * -1));
    // Update total display
    updateTotalPrice();
  }
});

// Remove item button
$( '#add-tickets-list' ).on( 'click', '.delete-list-item', function(e) {
  e.preventDefault();
  const listItem = $( this ).parent();
  // Update available tickets
  updateAvailableTickets(listItem.data('date-id'), listItem.data('quantity'));
  // Remove the item from the list
  listItem.remove();
  // Update the visual total
  updateTotalPrice();
});

// Add to basket button
$( '#addTicketsToBasket' ).click(function() {
  const modal = $('#add-ticket-modal');
  const ticketList = $( "#add-tickets-list" );
  // Is there anything to add
  if (ticketList.children("li").length) {
    // Format the data for the Basket
    // Send to server
    // Redirect to basket
  }
  // Hide modal if no tickets to add
  modal.modal('hide');
});













