
/*
 * Provides code for a simple number spinner field
 */


function setValue(target, value) {
  const min = parseInt(target.attr('min')) || -Infinity;
  const max = parseInt(target.attr('max')) || Infinity;

  if (value < min) value = min;
  if (value > max) value = max;
  target.val(value);
}

function stepValue(target, step) {
  setValue(target, parseInt(target.val()) + step)
}

$( '.input-number-control :button.btn-dec' ).click(function() {
  const element = $( this ).siblings($( this ).data('target'));
  const step = -(parseInt(element.attr('step')) || 1);

  stepValue(element, step);
});
$( '.input-number-control :button.btn-inc' ).click(function() {
  const element = $( this ).siblings($( this ).data('target'));
  const step = (parseInt(element.attr('step')) || 1);

  stepValue(element, step);
});
$( '.input-number-control :input[type="number"]' ).change(function() {
  const element = $( this );

  setValue( element, parseInt(element.val()) );
});