(function($) {
  $(document).ready(function () {
    $('.post').each(function (_, post) {
      $(post).find('.hide_button').click(function() {
        $(post).css({ display: 'none' });
      });
    });
  });
})(jQuery);
