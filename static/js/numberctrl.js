
/*
 * Provides code for a simple number spinner field
 */

function spinnerBtn(target, step) {
  const min = parseInt(target.attr('min'));
  const max = parseInt(target.attr('max'));
  let value = parseInt(target.val()) + step;

  if (value < min) value = min;
  if (value > max) value = max;

  target.val( value );
}

$( 'button.btn-dec' ).click(function() {
  spinnerBtn($( this ).siblings($( this ).data('target')), -1);
});
$( 'button.btn-inc' ).click(function() {
  spinnerBtn($( this ).siblings($( this ).data('target')), 1);
});