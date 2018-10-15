$(function() {
        
  $('.list-group-item').on('click', function() {
    $('.fa', this)
      .toggleClass('fa-caret-right')
      .toggleClass('fa-caret-down');
  });

});