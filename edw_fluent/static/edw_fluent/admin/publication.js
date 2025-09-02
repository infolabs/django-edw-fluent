if (jQuery != undefined) {
  var django = {
    'jQuery': jQuery,
  }
}

(function($) {
  $(document).ready(function() {
    var $container = $('.field-description > div'),
        $widget = $container.find('.django-ckeditor-widget'),
        $helpText = $container.find('.help'),
        $showTogglerText = "<span class='show-module-toggler show-description'>Показать</span>";
    $widget.hide();
    $helpText.hide();
    $container.append($showTogglerText);

    $container.on('click', '.show-description', function() {
      $widget.show();
      $helpText.show();
      this.remove();
    });
  });
})(django.jQuery);
