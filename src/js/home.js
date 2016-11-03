$(document).ready(function() {
    var erweima;
    function loadQrcode() {
        erweima = layer.open({
            content: "<div class='close_wrapper'><img src='/static/img/erweima.png' style='width: 100%'></img><div class='close'></div></div>",
        })
    }

    $(".info").on("click", function() {
        loadQrcode();
    })

    $(document).on("click", '.close', function() {
        layer.close(erweima)
    })

    $(".footer a").on("click", function() {
        loadQrcode();
    })




});
