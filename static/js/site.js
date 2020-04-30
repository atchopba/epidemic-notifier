$(document).ready(function(){

    // bouton commencer notification
    $("#btnnotif").click(function() {

        $("#box_searching").show();
        $("#box_searching").html("Les notifications sont en cours d'envoie aux personnes concernées ...!");

        $.ajax({
            url: "/notifications/add",
            type: "POST",
            /*data: {
                q: search_text
            },*/
            success : function(data) {
                alert("Notification réalisée avec succès !");
                location.reload();
            },
            error: function(result, status, error) {
                $("#box_searching").css("display", "none");
                alert("Une erreur est survenue. Veuillez ressayer!");
            }
        });
    });

});