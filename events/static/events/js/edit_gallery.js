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