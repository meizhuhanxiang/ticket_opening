$(document).ready(function() {
    var timeID = null;
    function slideRight() {
        clearTimeout(timeID);
        timeID = setTimeout(function() {
            $.fn.fullpage.moveSlideRight()
        }, 1500)
    }
    $('#fullpage').fullpage({
        verticalCentered: false,
        scrollOverflow: true,
        css3:true,
        loopBottom: true,
        afterLoad: function(anchorLink, index) {
            if (index == 2) {
                var loadedSlide = $(this);
                $("#section2 #slide1 .person1").addClass("animated slideInDown").css("visibility", "visible")
                $("#section2 #slide1 .person2").addClass("animated slideInUp").css("visibility", "visible")
                $("#section2 #slide1 .name").addClass("animated slideInUp").css("visibility", "visible")
                slideRight()
            }
            if (index == 3) {
                $("#section3 .white-bg").addClass("animated fadeIn").css("visibility", "visible");
                setTimeout(function() {
                    $("#section3 .text-title").addClass("animated fadeIn").css("visibility", "visible");
                }, 1000)
                setTimeout(function() {
                    $("#section3 .bonus").addClass("animated fadeIn").css("visibility", "visible");
                }, 2000)
                setTimeout(function() {
                    $("#section3 .explain-text").addClass("animated fadeIn").css("visibility", "visible");
                }, 3000)
            }
        },

        afterSlideLoad: function(anchorLink, index, slideAnchor, slideIndex) {
            var loadedSlide = $(this);

            //first slide of the second section
            if (index == 2 && slideIndex == 1) {
                $("#section2 #slide2 .person1").addClass("animated slideInDown").css("visibility", "visible")
                $("#section2 #slide2 .person2").addClass("animated slideInUp").css("visibility", "visible")
                $("#section2 #slide2 .name").addClass("animated slideInUp").css("visibility", "visible")
                slideRight()
            }
            if (index == 2 && slideIndex == 2) {
                $("#section2 #slide3 .person1").addClass("animated slideInDown").css("visibility", "visible")
                $("#section2 #slide3 .person2").addClass("animated slideInUp").css("visibility", "visible")
                $("#section2 #slide3 .name").addClass("animated slideInUp").css("visibility", "visible")
                slideRight()
            }
            if (index == 2 && slideIndex == 3) {
                $("#section2 #slide4 .person1").addClass("animated slideInDown").css("visibility", "visible")
                $("#section2 #slide4 .person2").addClass("animated slideInUp").css("visibility", "visible")
                $("#section2 #slide4 .name").addClass("animated slideInUp").css("visibility", "visible")
                slideRight()
            }
            if (index == 2 && slideIndex == 4) {
                $("#section2 #slide5 .person1").addClass("animated slideInDown").css("visibility", "visible")
                $("#section2 #slide5 .person2").addClass("animated slideInUp").css("visibility", "visible")
                $("#section2 #slide5 .name").addClass("animated slideInUp").css("visibility", "visible")
                slideRight()
            }
            if (index == 2 && slideIndex == 5) {
                $("#section2 #slide6 .person1").addClass("animated slideInDown").css("visibility", "visible")
                $("#section2 #slide6 .person2").addClass("animated slideInUp").css("visibility", "visible")
                $("#section2 #slide6 .name").addClass("animated slideInUp").css("visibility", "visible")
                slideRight()
            }
        }
    });

    setTimeout(function() {
        $(".hand").hide();
        $("#section1").append('<img class="animated bounceInDown board" src="static/img/section/section1/section1-board.png" />')

    }, 2000)
    $("#music").on("click", function() {
        var audio = document.getElementById("audio");;
        if(audio.paused) {
            audio.play();
            $(this).addClass("rotate");
        } else {
            audio.pause();
            $(this).removeClass("rotate");
        }
    })
    $(".slide-down").on("click", function() {
        $.fn.fullpage.moveSectionDown()
    })
})