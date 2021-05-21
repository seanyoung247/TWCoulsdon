function spinnerBtn(target, step) {
  const min = parseInt(target.attr('min'));
  const max = parseInt(target.attr('max'));
  let value = parseInt(target.val()) + step;

  if (value >= min && value <= max) target.val( value );
}