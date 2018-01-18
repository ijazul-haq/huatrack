$(document).ready(function () {
    $('.slider').slider();
    $('.modal').modal();
    $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 15, // Creates a dropdown of 15 years to control year,
        today: 'Today',
        clear: 'Clear',
        close: 'Ok',
        closeOnSelect: true, // Close upon selecting a date,
        format: 'yyyy-mm-dd'
    });

    $("#asset-create").click(function (e) {
        e.preventDefault();
        var URL = $(this).attr('href');
        $.ajax({
            url: URL,
            dataType: 'json',
            beforeSend: function () {
                $("#bc-action").fadeOut()
                $("#bc-info").addClass('loading')
                $("#bc-info").html('Almost done! refresh the page after a few seconds')
                $("#bc-info").removeClass('hide')
                console.log('processing.......')
            },
            success: function (data) {
                $("#bc-info").removeClass('loading')
                if (data.status) {

                }
            }
        });
    });
});
        