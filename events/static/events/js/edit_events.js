/*
 * Provides code for the edit events page
 */

 //Initialises the rich text input field
tinymce.init({
  selector: '#id_description',
  plugins: 'advlist autolink lists link image charmap preview hr anchor',
  toolbar_mode: 'floating',
});