$(function(){
    $('#toggler-box').click(function(){
        $('#toggler').toggleClass('on');
        $('body').toggleClass('color-scheme-dark');
    });

    $('#drop').click(function(){
        $('#dropdown').toggleClass('slide');
        $('#dropdown').slideToggle();
    });

    // Mobile slides
    $('#admin-mobile').click(function(){
        $('#admin-mobile-slide').slideToggle();
        $('#att-mobile-slide').slideUp();
    });

    $('#att-mobile').click(function(){
        $('#att-mobile-slide').slideToggle();
        $('#admin-mobile-slide').slideUp();
    });
    // End mobile slides

    // Main popouts
    $('#admin-main').mouseenter(function(){
        $('#admin-main').addClass('active');
    });

    $('#admin-main').mouseleave(function(){
        $('#admin-main').removeClass('active');
    });

    $('#att-main').mouseenter(function(){
        $('#att-main').addClass('active');
    });

    $('#att-main').mouseleave(function(){
        $('#att-main').removeClass('active');
    });
    // End main popouts

});