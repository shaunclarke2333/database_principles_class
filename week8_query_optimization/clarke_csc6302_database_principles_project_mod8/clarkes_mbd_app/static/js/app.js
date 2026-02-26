/*-----------------------------------------------------------------------------------
    Template Name: Gymnast
    Template URL: https://themeforest.net/item/gymnast-gym-fitness-bodybuilding-yoga-and-nutrition-bootstrap-4-template/29543605
    Description: GYM, Fitness, Bodybuilding, Yoga and Nutrition Bootstrap 4 Template
    Author: Bull-Theme
    Author URI: https://themeforest.net/user/bull-theme
    Version: 1.0.0
-----------------------------------------------------------------------------------*/

(function($) {
    "use strict";

    $(document).ready(function() {

        /* ===============================  Before After Effect  =============================== */
        $(".before-after-effect").twentytwenty();

        /* ===============================  Timeline Owl Carousel =============================== */
        $('#timeline').owlCarousel({
            center: true,
            dots: true,
            nav: true,
            items: 1,
            loop: true,
            margin: 0,
            responsiveClass:true,
            responsive: {
                0 : {
                    items: 1
                },
                576 : {
                    items: 2
                },
                768 : {
                    items: 2
                },
                992 : {
                    items: 3
                },
                1200 : {
                    items: 4
                },
            }
        });

        /* =============================== Product, Related, Upsell and Cros sell Owl Carousel =============================== */
        $('#product-owlCarousel, #related-owlCarousel, #upsell-owlCarousel, #crosssell-owlCarousel').owlCarousel({
            lazyLoad: true,
            dots: true,
            nav: true,
            loop: true,
            margin: 30,
            items: 1,
            responsiveClass:true,
            responsive: {
                0 : {
                    items: 2,
                },
                576 : {
                    items: 2
                },
                768 : {
                    items: 2
                },
                992 : {
                    items: 2
                },
                1200 : {
                    items: 4
                },
            }
        });

        /* ===============================  Home 2 Slider =============================== */
        $('#bt-carousel-00dc4').owlCarousel({
            center: true,
            dots: true,
            dotsData: true,
            nav: false,
            lazyLoad: true,
            items: 1,
            loop: false,
            rewind: true,
            autoplay: true,
            autoplayTimeout: 10000,
            autoplayHoverPause: true,
            smartSpeed: 450,
            margin: 0,
        });

        /* ===============================  Magnific Popup =============================== */
        $('.popup-image').magnificPopup({
            type: 'image',
            mainClass: 'mfp-fade',
            removalDelay: 160,
            fixedContentPos: false
        });

        $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
            disableOn: 700,
            type: 'iframe',
            mainClass: 'mfp-fade',
            removalDelay: 160,
            preloader: false,
            fixedContentPos: false
        });

        /* ===============================  Light Gallery =============================== */
        $(".lightgallery").lightGallery({
            download: false,
            rotate: false
        });


    });

    // === window When Loading === //
    $(window).on("load", function () {

        /* ===============================  SPLITTING TEXT =============================== */
        Splitting();
        
    });

}(jQuery));



$(document).ready(function() {
        var e = document.querySelectorAll('[data-toggle="countup"]');

        function o(e) {
            var t = e.dataset.from ? +e.dataset.from : null,
                o = e.dataset.to ? +e.dataset.to : null,
                n = e.dataset.decimals ? +e.dataset.decimals : null,
                a = e.dataset.duration ? +e.dataset.duration : null,
                i = e.dataset.options ? JSON.parse(e.dataset.options) : null,
                l = new CountUp(e, t, o, n, a, i);
            l.error ? console.error(l.error) : (l.start(), e.classList.add("counted"))
        }
        "undefined" != typeof CountUp && e && [].forEach.call(e, function(e) {
            "countup:in" !== e.getAttribute("data-aos-id") && o(e)
        }), document.addEventListener("aos:in:countup:in", function(e) {
            if (e.detail instanceof Element) o(e.detail);
            else {
                var t = document.querySelectorAll('.aos-animate[data-aos-id="countup:in"]:not(.counted)');
                [].forEach.call(t, function(e) {
                    o(e)
                })
            }
        })
    

});



/* ===============================  Scroll back to top  =============================== */

$(document).ready(function () {
    "use strict";

    var progressPath = document.querySelector('.progress-wrap path');
    var pathLength = progressPath.getTotalLength();
    progressPath.style.transition = progressPath.style.WebkitTransition = 'none';
    progressPath.style.strokeDasharray = pathLength + ' ' + pathLength;
    progressPath.style.strokeDashoffset = pathLength;
    progressPath.getBoundingClientRect();
    progressPath.style.transition = progressPath.style.WebkitTransition = 'stroke-dashoffset 10ms linear';
    var updateProgress = function () {
        var scroll = $(window).scrollTop();
        var height = $(document).height() - $(window).height();
        var progress = pathLength - (scroll * pathLength / height);
        progressPath.style.strokeDashoffset = progress;
    }
    updateProgress();
    $(window).scroll(updateProgress);
    var offset = 150;
    var duration = 550;
    jQuery(window).on('scroll', function () {
        if (jQuery(this).scrollTop() > offset) {
            jQuery('.progress-wrap').addClass('active-progress');
        } else {
            jQuery('.progress-wrap').removeClass('active-progress');
        }
    });
    jQuery('.progress-wrap').on('click', function (event) {
        event.preventDefault();
        jQuery('html, body').animate({ scrollTop: 0 }, duration);
        return false;
    })


});


/* ===============================  Mouse effect  =============================== */

function mousecursor() {
    if ($("body")) {
        const e = document.querySelector(".cursor-inner"),
            t = document.querySelector(".cursor-outer");
        let n, i = 0,
            o = !1;
        window.onmousemove = function (s) {
            o || (t.style.transform = "translate(" + s.clientX + "px, " + s.clientY + "px)"), e.style.transform = "translate(" + s.clientX + "px, " + s.clientY + "px)", n = s.clientY, i = s.clientX
        }, $("body").on("mouseenter", "a, .cursor-pointer", function () {
            e.classList.add("cursor-hover"), t.classList.add("cursor-hover")
        }), $("body").on("mouseleave", "a, .cursor-pointer", function () {
            $(this).is("a") && $(this).closest(".cursor-pointer").length || (e.classList.remove("cursor-hover"), t.classList.remove("cursor-hover"))
        }), e.style.visibility = "visible", t.style.visibility = "visible"
    }
};

$(function () {
    mousecursor();
});


/* =============================== Pie Chart =============================== */
$(function() {
    $('.pie-chart').easyPieChart({
        //your options goes here
    });
});

