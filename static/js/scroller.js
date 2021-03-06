/*
 * Provides code for a basic "netflix" style horizontal item scroller.
 */

// Scrolls one "page" left (backwards)
$( ".scroller .scroll-left" ).click(function(event) {
  const scroller = $( this ).siblings( ".scroller-items" );
  const scrollItem = scroller.children( ".scroll-item" );
  //const scrollEndItem = scroller.children( ".scroll-item-bookend" );
  let scrollPosition = scroller.get(0).scrollWidth;
  // If we're at the beginning of the items, move back one page
  if (scroller.scrollLeft() > 0) {
    // Which item is left most?
    let leftMostItem = Math.ceil((scroller.scrollLeft()) / scrollItem.outerWidth());
    // How many items fit in a page?
    let pageItemWidth = Math.floor(scroller.width() / scrollItem.outerWidth());
    // Calculate new scroll position: Find out which item should be left most
    //  then calulate it's position by multiplying it by icon width
    scrollPosition = ((leftMostItem - pageItemWidth) * scrollItem.outerWidth());
  }
  scroller.animate({scrollLeft: scrollPosition}, 500);
});

// Scrolls one "page" right (forwards)
$( ".scroller .scroll-right" ).click(function(event) {
  const scroller = $( this ).siblings( ".scroller-items" );
  const scrollItemWidth = scroller.children( ".scroll-item" ).outerWidth();
  const scrollEndPosition = scroller.scrollLeft() + scroller.width() +
    scroller.children( ".scroll-item-bookend" ).outerWidth();
  let scrollPosition = 0;
  // If we're not at the end of the items move to the next page
  if (scrollEndPosition < (scroller.get(0).scrollWidth - 1)) {
    // Which item is left most?
    let leftMostItem = Math.floor((scroller.scrollLeft()) / scrollItemWidth);
    // How many items fit in a page?
    let pageItemWidth = Math.floor(scroller.width() / scrollItemWidth);
    // Calculate new scroll position: Find out which item should be left most
    //  then calulate it's position by multiplying it by icon width
    scrollPosition = ((leftMostItem + pageItemWidth) * scrollItemWidth);
  }
  scroller.animate({scrollLeft: scrollPosition}, 500);
});

// TODO: Add scroll to item function