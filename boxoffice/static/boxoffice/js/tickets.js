/*
 * Provides code for adding and removing tickets from the basket.
 */

// Clears the ticket list
function clearTicketList() {
  $('#add-ticket-modal').find( '#add-tickets-list' ).html("");
  $('#add-ticket-modal').find( '#add-tickets-total' ).text("0.00");
}

// Shows the add tickets modal and requests event data from the server.
$( '.btn-add-tickets' ).click( function() {
  const modal = $('#add-ticket-modal');
  const url = `/boxoffice/buy_tickets/?event=${$( this ).data('event-id')}`;
  var show_modal = true;

  // Set the modal title
  modal.find( '.modal-title' ).text( $( this ).data('event-title') );

  // Set the modal to it's preloaded state
  modal.find( '#add-tickets-form-wrapper' ).html("<h5>Loading...</h5>");
  clearTicketList();

  // Request modal HTML from server
  $.get( url, function(data) {
    const formWrapper = $('#add-tickets-form-wrapper');
    // Did we recieve the form?
    if (data.success) {
      formWrapper.html(data.form);
      // Don't let the user select more tickets than there are
      $( '#add-ticket-quantity' ).attr(
        'max', $( '#add-ticket-date' ).find( ':selected' ).data('tickets-left'));
    } else {
      addMessage(data.message_html);
      // Give the modal a chance to be shown then hide it
      setTimeout(function() {$('#add-ticket-modal').modal('hide')}, 1000);
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
  const qtyInput = $( '#add-ticket-quantity' );
  const ticketsLeft = $( '#add-ticket-date' ).find( ':selected' ).data('tickets-left')
  qtyInput.attr('max', ticketsLeft);
  if (qtyInput.val() > ticketsLeft) qtyInput.val(ticketsLeft);
});

/*
 * Spinner controls for the number field
 */
$( '#add-tickets-form-wrapper' ).on( 'click', 'button.btn-dec', function(e) {
  e.preventDefault();
  stepValue($( $( this ).data('target') ), -(parseInt($( this ).attr('step')) || 1));
});
$( '#add-tickets-form-wrapper' ).on( 'click', 'button.btn-inc', function(e) {
  e.preventDefault();
  stepValue($( $( this ).data('target') ), (parseInt($( this ).attr('step')) || 1));
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
  const newCount = parseInt(dateOption.data('tickets-left')) + adjustment;

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
    else {
      const qtyInput = $( '#add-ticket-quantity' )
      qtyInput.attr('max', newCount);
      if (qtyInput.val() > newCount) qtyInput.val(newCount);
    }
  }
}

// Updates visual price
function updateTotalPrice() {
  const ticketList = $( '#add-tickets-list' );
  let total = 0;

  // Traverse the list, getting the price and quantity of each item
  ticketList.children('.add-ticket-list-item').each(function() {
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
      // Append the list item
      $( '#add-tickets-list' ).append(listItem);
    }

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
    let items = [];
    // Format the data for the Basket
    ticketList.children('.add-ticket-list-item').each(function() {
      const date_id = $( this ).data('date-id');
      const ticket_id = $( this ).data('ticket-id');
      const quantity = $( this ).data('quantity');

      items.push({
        date_id: date_id,
        type_id: ticket_id,
        quantity: quantity
      });
    });
    // Send to server
    const postData = {
      'csrfmiddlewaretoken': csrfToken,
      'tickets': JSON.stringify(items)
    };
    $.post( '/boxoffice/basket/add/', postData, function(data) {
      if (data.success) {
        // Adding tickets succeeded
        window.location.href = '/boxoffice/basket';
      } else {
        // Adding tickets failed
        addMessage(data.message_html);
      }
    });
  }
});
