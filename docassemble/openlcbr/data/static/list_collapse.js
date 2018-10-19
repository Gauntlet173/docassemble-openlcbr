/*
$(function() {
        
  $('.list-group-item').on('click', function() {
    $('.fa', this)
      .toggleClass('fa-caret-right')
      .toggleClass('fa-caret-down');
  });

});
*/
$(function() {
  
  $('.list-group-item').on('click', function() {
  
    var icon = $(this).find('.svg-inline--fa');
    var icon_fa_icon = icon.attr('data-icon');

    if (icon_fa_icon === "caret-right") {
        icon.attr('data-icon', 'caret-down');
    } else {
        icon.attr('data-icon', 'caret-right');
    }
  });

});