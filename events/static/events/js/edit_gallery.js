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

// Clears the image upload form
function clearUploadForm() {
  // Clear the upload form
  $( '#image-upload' ).val('');
  // Clear the name field
  $( '#gallery-admin-title' ).val('');
  // Clear the preview image
  $( '#gallery-image' ).attr('src', '');
  // Show the add file button
  $( '#gallery-add-image-btn' ).show();
}

// Hook into the gallery-image event so we can set admin
// tools when the gallery is shown
$('.scroller-items').on('click', '.gallery-image-link', function() {
  const current = $( this );
  const currentData = current.data('description');
  const currentIndex = $( '.scroller-items li' ).index(current.parent());
  const titleInput = $( '#gallery-admin-title' );
  const addImageBtn = $( '#gallery-add-image-btn' );
  const updateImageBtn = $( '#gallery-admin-update' );
  const deleteImageBtn = $( '#gallery-admin-delete' );
  const titleImageBtn = $( '#gallery-title-image-btn' );

  // Set the contents of the image title input
  titleInput.attr('placeholder', 'Image name');
  titleInput.val(currentData);

  // Tag the buttons with the current gallery item index
  // (simplifies updating/deleting it)
  updateImageBtn.data('index', currentIndex);
  deleteImageBtn.data('index', currentIndex);
  // Clear the file upload, don't stash selected files
  $( '#image-upload' ).val('');
  // Is this the add image button
  if (current.data('admin') == 'True') {
    // Show the add image button
    addImageBtn.show();
    // Hide the title image button
    titleImageBtn.hide();
    // Update button adds images here:
    updateImageBtn.text("Add");
    // Delete button clears the selected file
    deleteImageBtn.text('Cancel');
    titleInput.val('');
  } else {
    // Hide the add image button
    addImageBtn.hide();
    titleImageBtn.show();
    updateImageBtn.text('Update');
    deleteImageBtn.text('Delete');
  }
});

// Title-image button clicked
$( '#gallery-title-image-btn' ).click(function() {
  const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  const event_id = $('input[name="event_id"]').val();
  const galleryImage = $('#gallery-image');
  const current = $( this );

  if (galleryImage.data('id') > 0) {
    // Try to update the event record
    const url = current.data('update-url');
    const postData = {
      'csrfmiddlewaretoken': csrfToken,
      'event_id': event_id,
      'image_id': galleryImage.data('id'),
    };
    $.post(url, postData).done(function(data) {
      // If successful reflect the change in the event title
      if (data.success) {
        // Get the event's title image and set it's background
        // to the src of the gallery image tag
        $( '.event-header' )
          .css('background-image', `url(${galleryImage.attr('src')})`);
      }
      addMessage(data.message_html);
    });
  }
});

// Add image button clicked
$( '#gallery-add-image-btn' ).click(function() {
  // Show the file dialog
  $( '#image-upload' ).click();
});

// File has been selected
$( '#image-upload' ).change(function() {
  const [file] = this.files;
  // If a file was selected add it as a preview
  if (file) {
    $( '#gallery-image' ).attr('src', URL.createObjectURL(file));
    // Hide the add file button
    $( '#gallery-add-image-btn' ).hide();
  }
});

// Update button clicked
$( '#gallery-admin-update' ).click(function() {
  const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  const image_id = $('#gallery-image').data('id');
  const titleInput = $( '#gallery-admin-title' );
  const current = $( this );

  if (image_id > 0) {
    // Try to update the image
    const url = current.data('update-url');
    const postData = {
      'csrfmiddlewaretoken': csrfToken,
      'image_id': image_id,
      'image-name': titleInput.val()
    };
    $.post(url, postData).done(function(data) {
      // If successful reflect the change in the list
      if (data.success) {
        // Get the gallery link item
        const currentLink = $( '.scroller-items li' ).eq(current.data('index'));
        // Update the description data variable
        currentLink.children('a.gallery-image-link').data('description', titleInput.val());
      }
      addMessage(data.message_html);
    });
  } else {
    // Try to submit a new image
    $( '#image-upload-form' ).submit();
  }
});

// Delete button clicked
$( '#gallery-admin-delete' ).click(function() {
  const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  const image_id = $('#gallery-image').data('id');
  const current = $( this );

  if (image_id > 0) {
    // Try to remove the image
    const url = current.data('remove-url');
    const postData = {
      'csrfmiddlewaretoken': csrfToken,
      'image_id': image_id
    };
    $.post(url, postData).done(function(data) {
      if (data.success) {
        // Get the tile to delete
        const currentIndex = current.data('index');
        const currentLink = $( '.scroller-items li' ).eq(currentIndex);
        // Remove the tile
        currentLink.remove();
        // Move to the next free tile
        // Get the item that is now at this index, and activate it's click event
        $( '.scroller-items li' ).eq(currentIndex)
          .children('a.gallery-image-link').click();
      }
      addMessage(data.message_html);
    });
  } else {
    // Clear the file upload form
    clearUploadForm();
  }
});

// Captures the form submission so it can be done asynchronously
$( '#image-upload-form' ).submit(function(e) {
  e.preventDefault();
  this.reportValidity();
  // Can we submit the form?
  const fileInput = $( '#image-upload' );
  const titleInput = $( '#gallery-admin-title' );
  const [file] = fileInput[0].files;
  // If there's file data, submit it
  if (file && titleInput.val()) {
    // Submit it
    $.ajax({
      url: $( this ).attr('action'),
      cache: false,
      processData: false,
      contentType: false,
      data: new FormData(this),
      type: "POST",
      success: function(data) {
          // Was the image added successfully?
          if (data.success) {
            // Get the new gallery tile html and add it to the gallery list
            const newImage = $( data.item_html );
            newImage.insertBefore('.scroll-item:last');
            clearUploadForm();
            // Update gallery links
            // $( '#gallery-prev' ).data('target',
            //   $('#add-image-item').prev().children('.gallery-image-link'));
            $('#add-image-item').children('.gallery-image-link').click();
          }
          addMessage(data.message_html);
      }
    });
  }
});
