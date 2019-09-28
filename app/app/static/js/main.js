$(function () {
    var formx = $("#wizard").show();
    var foam = $('#forms').show();
    formx.steps({
        headerTag: "h4",
        bodyTag: "section",
        transitionEffect: "fade",
        // enableAllSteps: true,
        transitionEffectSpeed: 500,
        onStepChanging: function (event, currentIndex, newIndex) {
            if (currentIndex > newIndex) {
                $('.actions ul').addClass('actions-next');
                return true;
            } 
            if (currentIndex < newIndex) {
                formx.find(".body:eq(" + newIndex + ") label.error").remove();
                formx.find(".body:eq(" + newIndex + ") .error").removeClass("error");
            }
            foam.validate().settings.ignore = ":disabled,:hidden";
            return foam.valid();

        },
        labels: {
            finish: "Submit",
            next: "Continue",
            previous: "Back"
        }, 
        onFinishing: function (event, currentIndex)
        {
            foam.validate().settings.ignore = ":disabled";
            return foam.valid();
        },
        onFinished: function (event, currentIndex) {
            document.getElementById("forms").submit();
            alert("submitted");
        }
    });

    // Custom Steps 
    $('.wizard > .steps li a').click(function () {
        $(this).parent().addClass('checked');
        $(this).parent().prevAll().addClass('checked');
        $(this).parent().nextAll().removeClass('checked');
    });
    // Custom Button Jquery Step
    $('.forward').click(function () {
        $("#wizard").steps('next');
    });
    $('.backward').click(function () {
        $("#wizard").steps('previous');
    });
    // Input Focus
    $('.form-holder').delegate("input", "focus", function () {
        $('.form-holder').removeClass("active");
        $(this).parent().addClass("active");
    });


    $('#Fname').keyup(function () {
        $('#FnameDisplay').text($(this).val());
    });
    $('#Lname').keyup(function () {
        $('#LnameDisplay').text($(this).val());
    });
    $('#studentID').keyup(function () {
        $('#studentIDDisplay').text($(this).val());
    });
    $('#contact_no').keydown(function () {
        $('#contact_noDisplay').text($(this).val());
    });
    $('#year').keydown(function () {
        $('#yearDisplay').text($(this).val());
    });
    
    var courseName = $('#course option:selected').text();
    $('CourseDisplay').text(courseName);
});