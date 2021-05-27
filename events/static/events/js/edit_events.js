/*
 * Provides code for the edit events page
 */

 //Initialises the rich text input field
tinymce.init({
  selector: '#id_description',
  plugins: 'advlist autolink lists link image charmap preview hr anchor',
  toolbar_mode: 'floating',
});

/*
 * Addiing dates
 */
// Add a new date
$( '#add-date-btn' ).click(function(e) {
  e.preventDefault();
  html=`
  <li class="add-date-item">
    <input name="event_date" class="form-control m-1" type="date" value="" required>
    <input name="event_time" class="form-control m-1" type="time" value="" required>
    <button class="remove-date-btn btn btn-twc-brand m-1" type="button">
      &times;
    </button>
  </li>`
  $( '#add-date-list' ).append(html);
});

// Remove a date
$( "#add-date-list" ).on('click', '.remove-date-btn', function() {
  $( this ).parent().remove();
});

/*
 * Adding to the gallery
 */
// Sets the preview when a file is selected
$( '#add-gallery-list' ).on('change', '.image-chooser', function() {
  const imagePreview = $( this ).siblings(".upload-image-preview");
  if (this.files && this.files[0]) {
    const src = URL.createObjectURL(this.files[0]);
    imagePreview.attr('src', src);
  }
});

// Clears the error hint on changing the required image fields
$( '#add-image-chooser' ).change(function() {
  $( this ).removeClass('add-image-invalid');
});
$( '#add-image-name' ).change(function() {
  $( this ).removeClass('add-image-invalid');
});

// Adds another image to the list
$( '#add-image-btn' ).click(function(e) {
  e.preventDefault();
  // Create the html for the new image item
  html = `
  <li class="upload-image-item">
    <div class="row">
      <label>
        <img class="upload-image-preview" src="${$(this).data('no-image')}">
        <input name="existing_image" type="hidden" value="none">
        <input class="image-chooser hidden-image-input" name="new_image" type="file"
                accept="image/png, image/jpeg" required>
      </label>
      <div class="col text-right">
        <input name="image_name" class="form-control mb-1" type="text" placeholder="Image name"
                value="" required>
        <input name="image_description" class="form-control mb-1"
                type="text" placeholder="Image description"
                value="">
        <div class="row">
          <div class="col-6 text-left">
            <label for="title_image">Use as title image</label>
            <input name="title_image" type="radio">
          </div>
          <div class="col-6 text-right">
            <button class="remove-image-btn btn btn-twc-brand" type="button">
              Remove
            </button>
          </div>
        </div>
      </div>
    </div>
  </li>`
  // Create the new element and add it to the list
  $( '#add-gallery-list' ).append(html)
});

// Remove an image from the gallery
$( '#add-gallery-list' ).on( 'click', '.remove-image-btn', function(e) {
  e.preventDefault();
  $( this ).closest( 'li.upload-image-item' ).remove();
});

// Captures the submit event so we can set the title image
const form = $( '#event-form' );
form[0].addEventListener('submit', function(e) {
  e.preventDefault();

  const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  let dates = [];
  let images = [];

  // Construct the list of event dates
  $( '#add-date-list' ).children('li').each(function(){
    const date = $( this ).children('input[name="event_date"]');
    const time = $( this ).children('input[name="event_time"]');
    dates.push({
      'date': $.trim(date.val()),
      'time': $.trim(time.val())
    });
  });
  // Construct the list of gallery images
  $( '#add-gallery-list' ).children('li').each(function() {
    images.push({
      'existing_image': $.trim($( this ).children('input[name="existing_image"]')),
      'new_image': $.trim($( this ).children('input[name="new_image"]')),
      'image_name': $.trim($( this ).children('input[name="image_name"]')),
      'image_description': $.trim($( this ).children('input[name="image_description"]')),
      'title_image': $.trim($( this ).children('input[name="title_image"]'))
    });
  });

  url = form.attr('action');
  // Construct the data to submit
  postData = {
    'csrfmiddlewaretoken': csrfToken,
    'title': $.trim(form[0].title.value),
    'author': $.trim(form[0].author.value),
    'tagline': $.trim(form[0].tagline.value),
    'description': $.trim(form[0].description.value),
    'type': $.trim(form[0].type.value),
    'venue': $.trim(form[0].venue.value),
    'content': $.trim(form[0].content.value),
    'dates': dates,
    'images': images
  }
  const event_id = $( 'input[name="event_id"' ).val();

  console.log(postData);
  if (event_id) postData['event_id'] = event_id;

  $.post(url, postData).done(function(data) {
  //  console.log(data);
  });


});
