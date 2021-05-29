/*
 * Provides code for dealing with the basket and items.
 */

// Updates the visual elements, such as the basket icon and total price
function update_basket() {
  const listItems = $( '#basket-list' ).children( '.basket-list-item' );
  let total_items = 0;
  // Are there any items left?
  if (listItems.length > 0) {
    let total = 0;
    // Go over the items in the list and recalculate the Total price
    listItems.each(function() {
      total_items += parseInt( $( this ).data('quantity') );
      total += parseFloat( $( this ).data('price') ) * parseInt( $( this ).data('quantity') );
    });
    $( '#basket-total span' ).text(total.toFixed(2));
  } else {
    $( '#basket-total span' ).text('0.00');
    // Clears the basket items notification circle
    $( 'svg .icon-ticket-alert' ).addClass('hide');
    // Add the no items text
    const html = '<li class="no-basket-items">You have no items in your basket.</li>';
    $( '#basket-list' ).append(html);
    // Remove the checkout button
    $( '#checkout-btn' ).remove();
  }
  // Finally update the window title
  document.title = `Basket (${total_items} items) - Theatre Workshop Coulsdon`;
}

// Update item button
$( '.basket-update-item' ).click(function() {
  // Get the nearest quantity control
  const listItem = $( this ).parents( '.basket-list-item' );
  const qtyInput = listItem.find('.item-line-quantity');
  const quantity = parseInt(qtyInput.val());

  // Update the basket
  const postData = {
    'csrfmiddlewaretoken': csrfToken,
    'date_id': listItem.data('date-id'),
    'type_id': listItem.data('type-id'),
    'quantity': quantity
  };
  $.post( '/boxoffice/basket/update/', postData, function(data) {
    if (data.success) {
      // Set the new ticket line quantity
      listItem.data('quantity', quantity);
      // Update the line total
      listItem.find('.item-line-total').text(
        (parseFloat(listItem.data('price')) * quantity).toFixed(2));
      update_basket();
      addMessage(data.message_html);
    } else {
      addMessage(data.message_html);
    }
  });

});

// Delete item button
$( '.basket-delete-item' ).click(function() {
  // Get the ticket line item
  const listItem = $( this ).parents( '.basket-list-item' );

  // Remove the item from the basket
  const postData = {
    'csrfmiddlewaretoken': csrfToken,
    'date_id': listItem.data('date-id'),
    'type_id': listItem.data('type-id')
  };

  $.post( "/boxoffice/basket/remove/", postData, function(data) {
    // If the server confirms the item has been removed, remove the list item
    if (data.success) {
      listItem.remove();
      addMessage(data.message_html);
      update_basket();
    }
  });
});
