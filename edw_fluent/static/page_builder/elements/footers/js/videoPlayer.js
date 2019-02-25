$(function() {
    $('.play-video').on('click', function(event) {
        event.preventDefault();
        var $that = $(this),
            type = $that.data('type'),
            videoUrl = $that.attr('href'),
            $video;

        if (type === 'youtube') {
            $video = '<iframe id="video-player" src="'+videoUrl+'?rel=0&amp;showinfo=0&amp;controls=1&amp;autoplay=1" frameborder="0" allowfullscreen></iframe>';
        } else if (type === 'vimeo') {
            $video = '<iframe id="video-player" src="'+videoUrl+'?autoplay=1&color=ffffff&title=0&byline=0&portrait=0&badge=0&embedded=true" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>';
        } else if (type === 'dailymotion') {
            $video = '<iframe id="video-player" src="'+videoUrl+'?autoplay=1&color=ffffff&title=0&byline=0&portrait=0&badge=0" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>';
        } else {
            $video = '<video id="video-player" controls autoplay> <source src="'+videoUrl+'">Your browser does not support the video tag.</video>';
        }

        $('.video-container').find('#video-player').remove();
        $('.video-container').prepend($video);
        $('.video-container').fadeIn();
    });

    $('.video-close').on('click', function(event) {
        event.preventDefault();
        $('.video-container').fadeOut(600, function() {
            $('#video-player').remove();
        });
    });
});