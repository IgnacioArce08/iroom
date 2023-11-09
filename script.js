function mostrarInfo(info) {
    $("#info").html(info);
    $("#info").fadeIn();
}

function ocultarInfo() {
    $("#info").fadeOut();
}

$(document).ready(function() {
    $(".imagen").hover(
        function() {
            var info = $(this).data("info");
            mostrarInfo(info);
        },
        function() {
            ocultarInfo();
        }
    );
});