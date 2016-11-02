$(document).ready(function() {
    var erweima;
    function loadQrcode() {
        erweima = layer.open({
            content: "<div class='close_wrapper'><img src='/static/img/erweima.png' style='width: 100%'></img><div class='close'></div><img src='/static/img/erweima_context.png' class='erweima_context'></img></div>",
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
