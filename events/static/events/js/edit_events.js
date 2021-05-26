/*
 * Provides code for the edit events page
 */

 //Initialises the rich text input field
tinymce.init({
  selector: '#id_description',
  plugins: 'advlist autolink lists link image charmap preview hr anchor',
  toolbar_mode: 'floating',
});

// Sets the preview when a file is selected
$( '#add-image-chooser' ).change(function() {
  const imagePreview = $( this ).siblings("#add-image-preview");
  if (this.files && this.files[0]) {
    const src = URL.createObjectURL(this.files[0]);
    imagePreview.attr('src', src);
  }
});