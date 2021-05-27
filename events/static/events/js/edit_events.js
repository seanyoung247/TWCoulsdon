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
    <input name="date_id" type="hidden" value="-1">
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

// Captures the submit event so we can set the title image
const form = $( '#event-form' );
form[0].addEventListener('submit', function(e) {
  e.preventDefault();

  const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  var dates = [];

  // Construct the list of event dates
  $( '#add-date-list' ).children('li').each(function(){
    const date = $( this ).children('input[name="event_date"]');
    const time = $( this ).children('input[name="event_time"]');
    const date_id = $( this ).children('input[name="date_id"]');
    dates.push({
      'date_id': $.trim(date_id.val()),
      'date': $.trim(date.val()),
      'time': $.trim(time.val())
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
    'dates': JSON.stringify(dates),
  }
  const event_id = $( 'input[name="event_id"' ).val();
  if (event_id) postData['event_id'] = event_id;

  $.post(url, postData).done(function(data) {
  //  console.log(data);
  });
});
