// Adds or alters a url parameter
function setURLParameter(param, value) {
  // Get the current url and parameters
  let url = new URL($(location).attr('href'));
  let params = url.searchParams;
  // Set the parameter value
  params.set(param, value);
  // Add the url to the current state without triggering a reload
  window.history.pushState({},"", url.href);
}

// Loads more search items
$( '#load-more-btn' ).click(function() {
  let loadBtn = $( this );
  let url = `${loadBtn.data('url')}?page=${loadBtn.data('page')}`;
  // Show the load more indicator
  $( loadBtn.data('indicator') ).removeClass('hide');
  // Get more search results
  $.get( url, function( data ) {
    let loadBtn = $( '#load-more-btn' );
    // If there's no more results hide the load more button
    if (!data.more_pages) loadBtn.addClass('hide');
    // If new results were returned, add them to the event-list
    if (data.pages) $( loadBtn.data('target') ).append(data.pages);
    // Hide the loading indicator
    $( loadBtn.data('indicator') ).addClass('hide');
  });
});

//TODO: button-less infinite scroll lazy loading