/**
 * confirmation de la suppression 
 * @param url 
 */
function confirm_delete(url) {
    if (confirm("Etes-vous sûr?")) {
        location(url);
    }
}

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

    // autocompletion
    $("#searchname").autocomplete({

        source: function(request, response) {
            
            $.ajax({
                url: "/personnes/search",
                type: 'POST',
                dataType: 'json',
                data: {
                    personne_id_1: $("#personne_id_1").val(),
                    search_name: $("#searchname").val()
                },
                success: function(data) {
                    response($.map(data, function(obj) {
                        return {
                            "label" : obj[1] +" "+ obj[2] +" - " + obj[3], 
                            "value" : obj[0]
                        };
                    }));
                },
                error: function(result, status, error) {
                    console.log('Extraction du nom erreur : ', error);
                }
            });

        },
        minLength: 3,
        position : {
            at : 'bottom',
            my : 'top'
        },
        select : function(event, ui){ // lors de la sélection d'une proposition
            console.log("=> select : ", ui);
            console.log("==> selected : ", ui.item.label, ui.item.value);
            
            $("#searchname").val(ui.item.label); // display the selected text
            $("#personne_id_2").val(ui.item.value); // save selected id to hidden input
            return false;
        }
    });

});