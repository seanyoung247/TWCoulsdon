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
$('.scroller-items').on('click', '.gallery-image-link', function() {
  const current = $( this );
  const currentData = current.data('description');
  const titleInput = $( '#gallery-admin-title' );
  const addImageBtn = $( '#gallery-add-image-btn' );
  const updateImageBtn = $( '#gallery-admin-update' );
  const deleteImageBtn = $( '#gallery-admin-delete' );

  // Set the contents of the image title input
  titleInput.attr('placeholder', 'Image name');
  titleInput.val(currentData);

  // Clear the file upload, don't stash selected files
  $( '#image-upload' ).val('');
  // Is this the add image button
  if (current.data('admin') == 'True') {
    // Show the add image button
    addImageBtn.show();
    // Update button adds images here:
    updateImageBtn.text("Add");
    // Delete button clears the selected file
    deleteImageBtn.text('Cancel');
    titleInput.val('');
  } else {
    // Hide the add image button
    addImageBtn.hide();
    updateImageBtn.text('Update');
    deleteImageBtn.text('Delete');
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

// Captures the form submission so it can be done asynchronously
$( '#image-upload-form' ).submit(function(e) {
  e.preventDefault();
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
          } else {
            addMessage(data.message_html);
          }
      }
    });
  }
});
