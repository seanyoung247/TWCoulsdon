
/*
 * Provides code for a simple gallery component based on a Bootstrap modal
 */

function getPreviousItem(current) {
  return current.parent('.scroll-item').prev().children('.gallery-image-link');
}

function getNextItem(current) {
  return current.parent('.scroll-item').next().children('.gallery-image-link');
}

$( '#gallery-next' ).click(function() {
  $( this ).data('target').click();
});

$( '#gallery-prev' ).click(function() {
  $( this ).data('target').click();
});

$('.gallery-image-link').click(function(){
  const current = $( this );
  const prevBtn = $( '#gallery-prev' );
  const nextBtn = $( '#gallery-next' );
  // Get the modal for displaying the image
  const imageModal = $( current.data( "target" ) );
  // Set the image and caption
  imageModal.find('img').attr('src', current.data( 'image' )).attr('alt', $( this ).data( 'description' ));
  imageModal.find('#gallery-image-title').text(current.data( 'description' ));
  // Set the previous and next links
  prevBtn.data( 'target', getPreviousItem(current));
  nextBtn.data( 'target', getNextItem(current));
  // Disable the next/prev buttons if at beginning or end of image list
  if (!prevBtn.data( 'target' ).length) prevBtn.prop('disabled', true);
  else prevBtn.prop('disabled', false);
  if (!nextBtn.data( 'target' ).length) nextBtn.prop('disabled', true);
  else nextBtn.prop('disabled', false);

  // Show the modal
  imageModal.modal();
});