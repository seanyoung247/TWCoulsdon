/*
 * Provides code for gallery editing
 */

// Initialising gallery editing
$( document ).ready(function() {
  // Adds an admin button to the end of the gallery scroller
  let addImageItem = $( '#add-image-item' );

  addImageItem.insertBefore('.scroll-item-bookend:last');
  addImageItem.removeClass('d-none');
});

// Hook into the gallery-image event so we can set admin
// tools when the gallery is shown
$( '.gallery-image-link' ).click(function(){
  const current = $( this );
  const currentData = current.data('description');
  const titleInput = $( '#gallery-admin-title' );
  const addImageBtn = $( '#gallery-add-image-btn' );
  // Set the contents of the image title input
  titleInput.val(currentData);
  // Is this the add image button
  if (currentData == 'Add new image') {
    // Show the add image button
    addImageBtn.show();
  } else {
    // Hide the add image button
    addImageBtn.hide();
  }
});

// Add image button clicked
$( '#gallery-add-image-btn' ).click(function() {
  // Show the file dialog
  $( '#image-upload' ).click();
  console.log($( '#image-upload' ));
});
