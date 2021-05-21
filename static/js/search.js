/*
 * Provides code to perform lazy-loading of search results.
 */

// Loads more search items
$( '#load-more-btn' ).click(function() {
  const loadBtn = $( this );
  const url = `${loadBtn.data('url')}?page=${loadBtn.data('page')}`;
  // Show the load more indicator
  $( loadBtn.data('indicator') ).removeClass('hide');
  // Get more search results
  $.get( url, function( data ) {
    const loadBtn = $( '#load-more-btn' );
    // If there's no more results hide the load more button
    if (!data.more_pages) loadBtn.addClass('hide');
    // If new results were returned, add them to the event-list
    if (data.pages) $( loadBtn.data('target') ).append(data.pages);
    // Hide the loading indicator
    $( loadBtn.data('indicator') ).addClass('hide');
  });
});
