/**
 * confirmation de la suppression 
 * @param url 
 */
function confirm_delete(url) {
    if (confirm("Etes-vous sûr?")) {
        location(url);
    }
}

/** 
 * Validates that the input string is a valid date formatted as "mm/dd/yyyy"
 * @source : https://stackoverflow.com/questions/6177975/how-to-validate-date-with-format-mm-dd-yyyy-in-javascript
 * @param dateString
 * @return boolean
 */
function is_valid_date(dateString) {
    // First check for the pattern
    if(!/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(dateString))
        return false;

    // Parse the date parts to integers
    var parts = dateString.split("/");
    var day = parseInt(parts[0], 10);
    var month = parseInt(parts[1], 10);
    var year = parseInt(parts[2], 10);

    // Check the ranges of month and year
    if(year < 1000 || year > 3000 || month == 0 || month > 12)
        return false;

    var monthLength = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ];

    // Adjust for leap years
    if(year % 400 == 0 || (year % 100 != 0 && year % 4 == 0))
        monthLength[1] = 29;

    // Check the range of the day
    return day > 0 && day <= monthLength[month - 1];
}

/**
 * Check if heure is valid
 * @param heure
 * @return boolean
 */
function is_valid_heure(heure) {
    return /^([0-1]?[0-9]|2[0-4]):([0-5][0-9])(:[0-5][0-9])?$/.test(heure);
}

/**
 * Check if email is valid
 * @source : https://stackoverflow.com/questions/46155/how-to-validate-an-email-address-in-javascript
 * @param email
 * return boolean
 */
function is_valid_email(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

/**
 * check if string is valid
 * @param str_  
 * @return boolean
 */
function is_valid_string(str_) {
    //return typeof str_ === 'string' || str_ instanceof String;
    return !/\d{3,}/.test(str_);
}

/**
 * check if phone number is valid
 * @param numphone
 * @return boolean
 */
function is_valid_numphone(numphone) {
    return true;
}

/**
 * Validate form relation
 * @return boolean
 */
function validate_form_relation() {
    if (!is_valid_string($("#libelle").val())) {
        alert("Le libelle n'est pas valide!");
        return false;
    }
    return true;
}

/**
 * Validate form personne
 * @return boolean
 */
function validate_form_personne() {
    // 
    if ($("#nom").val().trim() == "" || !is_valid_string($("#nom").val())) {
        alert("Le nom n'est pas valide!");
        return false;
    }
    //
    if (!is_valid_string($("#prenom").val())) {
        alert("Le prénom n'est pas valide!");
        return false;
    }
    //
    if (!is_valid_date($("#date_naiss").val())) {
        alert("La date de naissance n'est pas valide!");
        return false;
    }
    // 
    if (!is_valid_numphone($("#num_telephone").val())) {
        alert("Le numéro de téléphone n'est pas valide!");
        return false;
    }
    // 
    if (!is_valid_email($("#email").val())) {
        alert("L'adresse mail n'est pas valide!");
        return false;
    }
    return true;

}

/**
 * Validate form crp
 * @return boolean
 */
function validate_form_crp() {
    if ($("#id_relation").val().trim() == "") {
        alert("Veuillez selectionner une relation");
        return false;
    }
    //
    if (($("#personne_id_2").val().trim() == "" && validate_form_personne()) ||
        ($("#personne_id_2").val().trim() != "")) {

    } else {
        alert("Veillez renseigner la personne cible!");
        return false;
    }
    //
    if (!is_valid_date($("#date_contact").val())) {
        alert("La date n'est pas valide!");
        return false;
    }
    //
    if ($("#heure_contact").val().trim() != "" && !is_valid_heure($("#heure_contact").val())) {
        alert("L'heure n'est pas valide!");
        return false;
    }
    return true;
}

/**
 * Validate form test
 * @return boolean
 */
function validate_form_test() {
    // 
    if (!is_valid_date($("#date_test").val())) {
        alert("La date du test n'est pas valide!");
        return false;
    }
    // 
    if ($("#heure_test").val().trim() != "" && !is_valid_heure($("#heure_test").val())) {
        alert("L'heure du test n'est pas valide!");
        return false;
    }
    // 
    if (!is_valid_date($("#date_resultat").val())) {
        alert("La date du résultat n'est pas valide!");
        return false;
    }
    // 
    if ($("#heure_resultat").val().trim() != "" && !is_valid_heure($("#heure_resultat").val())) {
        alert("L'heure du résultat n'est pas valide!");
        return false;
    }
    // date's comparison
    var str_date_1 = $("#date_test").val().trim();
    if ($("#heure_test").val().trim() != "") {
        str_date_1 += " " + $("#heure_test").val()
    }
    var str_date_2 = $("#date_resultat").val().trim();
    if ($("#heure_resultat").val().trim() != "") {
        str_date_2 += " " + $("#heure_resultat").val();
    }
    var date_1 = new Date(str_date_1);
    var date_2 = new Date(str_date_2);
    if (date_1.getTime() > date_2.getTime()) {
        alert("La date et heure du résultat doit supérieur au test");
        return false;
    }
    //
    if (!($('input[name=resultat]:checked').length > 0)) {
        alert("Veuillez faire un choix sur le résultat!");
        return false;
    }
    return true;
}

$(document).ready(function(){
    
    // bouton reinitialiser la bdd
    $("#btnreinit_db").click(function() {

        if (confirm("Etes-vous sûr?")) {

            $.ajax({
                url: "/db",
                type: "POST",
                success : function(data) {
                    alert("Réinitialisation réalisée avec succès !");
                    location.reload();
                },
                error: function(result, status, error) {
                    alert("Une erreur est survenue. Veuillez ressayer!");
                }
            });
            
        }
    });

    // bouton commencer notification
    $("#btnnotif").click(function() {

        if (confirm("Etes-vous sûr?")) {

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

        }
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