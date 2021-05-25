/*
 * Provides code to show and hide information messages
 */
// Shows any messages on page load
$( document ).ready(function() {
  $( '.message' ).each(function() {
    const current = $( this );
    const timeout = current.data('timeout');
    current.addClass('show');
    if (timeout) setTimeout(() => closeMessage(current), timeout);
  });
});

// Hides a message when the close button is clicked. Uses delegated events so
// that messages can be added dynamically without reloading the page.
$( '.message-container' ).on( 'click', '.close-message', function(e) {
  closeMessage($( this ).parent());
});

// Adds the html for a message to the message container and shows it.
function addMessage(html) {
  // Construct the new element
  const newMessage = $( html );
  // Add it to the message container
  $( '.message-container' ).append(newMessage);
  // Show the message
  newMessage.addClass('show');
  const timeout = newMessage.data('timeout');
  if (timeout) setTimeout(() => closeMessage(newMessage), timeout);
}

// Closes the message passed
function closeMessage(message) {
  message.removeClass('show');
  message.fadeOut();
  setTimeout(function() {message.remove();}, 550);
}