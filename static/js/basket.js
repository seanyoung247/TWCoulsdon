/*
 * Provides code for dealing with the basket and items.
 */

// Updates the visual elements, such as the basket icon and total price
function update_basket() {
  // 
}

// Update item button
$( '.basket-update-item' ).click(function() {

});

$( '.basket-delete-item' ).click(function() {
  // Get the ticket line and it's data
  const listItem = $( this ).parents( '.basket-list-item' );
  const date_id = listItem.data('date-id');
  const type_id = listItem.data('type-id');

  // Remove the item from the basket
  const postData = {
    'csrfmiddlewaretoken': csrfToken,
    'date_id': date_id,
    'type_id': type_id
  }

  $.post( "/boxoffice/basket/remove/", postData, function(data) {
    // If the server confirms the item has been removed, remove the list item
    if (data.success) {
      listItem.remove();
      update_basket();
    }
  });
});