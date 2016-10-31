$(document).ready(function() {
    function loadQrcode() {
        layer.open({
            title: [
                '长按关注官方账号',
                'background-color:#182f52; color:#fff;'
            ],
            content: "<img src='/static/img/qrcode.png'></img><p>长按关注G-STEPS街舞社可随时咨询问题</p>",
        })
    }

    $(".info").on("click", function() {
        loadQrcode();
    })

    $(".footer a").on("click", function() {
        loadQrcode();
    })



});
