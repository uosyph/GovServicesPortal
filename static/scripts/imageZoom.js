$(document).ready(function () {
    $('.zoom-button').click(function () {
        var modal = $('#imageModal');
        var modalImg = $('#modalImage');
        modal.css('display', 'block');
        modalImg.attr('src', $(this).prev('.order-image').attr('src'));
        $('body').addClass('modal-open');
    });

    $('#closeButton, #imageModal').click(function (event) {
        if (!$(event.target).is('#modalImage')) {
            $('#imageModal').css('display', 'none');
            $('body').removeClass('modal-open');
        }
    });
});
