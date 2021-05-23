 /*
  * Provides functionality for a scroll to top button
  */

$( document ).ready(function() {
  $('[data-toggle="tooltip"]').tooltip();
  toggleScrollBtn();
});

// Toggles showing and hiding the scroll to top button based on whether
// the navbar is visible
function toggleScrollBtn() {
  if ( $( window ).scrollTop() > $( '.nav-wrapper' ).height() ) {
    $( '#scroll-to-top-btn' ).fadeIn();
  } else {
    $( '#scroll-to-top-btn' ).blur().fadeOut();
  }
}

 // Shows the scroll to top button only if the navbar is out of view
$( window ).scroll(function() {
  toggleScrollBtn();
});

$( '#scroll-to-top-btn' ).click(function() {
  $( window ).scrollTop(0,0);
});
