/*
 * Provides code to show and hide information messages
 */
// Shows any messages on page load
$( document ).ready(function() {
  $( '.message' ).addClass('show');
});

// Hides a message when the close button is clicked. Uses delegated events so
// that messages can be added dynamically without reloading the page.
$( '.message-container' ).on( 'click', '.close-message', function(e) {
  const message = $( this ).parent();
  message.removeClass('show');
  message.fadeOut();
  setTimeout(function() {message.remove();}, 550);
});

// Adds the html for a message to the message container and shows it.
function addMessage(html) {
  // Construct the new element
  const newMessage = $( html );
  // Add it to the message container
  $( '.message-container' ).append(newMessage);
  // Show the message
  newMessage.addClass('show');
}