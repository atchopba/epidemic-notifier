/**
 * confirmation de la suppression 
 * @param url 
 */
function confirm_delete(url) {
    if (confirm("Etes-vous sûr?")) {
        window.location.href = url;
    }
}

/**
 * Return the current date
 * @return date
 */
function get_current_date() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    return dd + '/' + mm + '/' + yyyy;
}

/**
 * Compare 2 date
 * @param str_date_1    
 * @param str_date_2
 * @return boolean
 */
function compare_date(str_date_1, str_date_2) {
    var date_1 = new Date(convert_date_fr_2_en(str_date_1));
    var date_2 = new Date(convert_date_fr_2_en(str_date_2));
    return date_1.getTime() >= date_2.getTime();
}

/**
 * Convert date fr to en
 * @param str_date  Date in fr
 * @return boolean
 */
function convert_date_fr_2_en(str_date) {
    var parts = str_date.split("/");
    var day = parseInt(parts[0], 10);
    var month = parseInt(parts[1], 10);
    var year = parseInt(parts[2], 10);
    return month + "/" + day + "/" + year;
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
    return day > 0 && day <= monthLength[month - 1] && compare_date(get_current_date(), dateString);
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
 * Validate form guerison of personne
 * @return boolean
 */
function validate_form_personne_guerison() {
    //
    if ($("#personne_id").val() == "") {
        alert("Il faut impérativement une personne renseignée!");
        return false;
    }
    //
    if (!is_valid_date($("#date_guerison").val())) {
        alert("La date de guérison n'est pas valide!");
        return false;
    }
    //
    if (!($('input[name=guerison_type_id]:checked').length > 0)) {
        alert("Veuillez faire un choix sur la guérison!");
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

/**
 * Validate form login
 * @return boolean
 */
function validate_form_login() {
    // 
    if ($("#login").val().trim() == "" || !is_valid_string($("#login").val())) {
        alert("Le login n'est pas valide!");
        return false;
    }
    //
    if ($("#mdp").val().trim() == "" || !is_valid_string($("#mdp").val())) {
        alert("Le mot de passe n'est pas valide!");
        return false;
    }
    return true;
}

/**
 * validate form personne consultation
 * @return boolean
 */
function validate_form_personne_consultation() {
    //
    if ($("#personne_id").val() == "") {
        alert("Il faut impérativement une personne renseignée!");
        return false;
    }
    // 
    if (!is_valid_date($("#date_consultation").val())) {
        alert("La date de consultation n'est pas valide!");
        return false;
    }
    return true;
}

/**
 * validate form personne vie condition
 * @return boolean
 */
function validate_form_pv_condition() {
    //
    if ($("#personne_id").val() == "") {
        alert("Il faut impérativement une personne renseignée!");
        return false;
    }
    //
    if ($("input[name=has_enfant]").is(":checked") && ($("#nb_enfant").val().trim() == "" || parseInt($("#nb_enfant").val().trim()) < 1)) {
        alert("Veuillez renseigner le nombre d'enfants!");
        return false;
    }
    //
    if ($("input[name=has_personne_agee]").is(":checked") && ($("#nb_personne_agee").val().trim() == "" || parseInt($("#nb_personne_agee").val().trim()) < 1)){
        alert("Veuillez renseigner le nombre de personne âgée!");
        return false;
    }
    return true;
}

/**
 * validate form personne symptome
 * @return boolean
 */
function validate_form_personne_diagnostic() {
    //
    if ($("#personne_id").val() == "") {
        alert("Il faut impérativement une personne renseignée!");
        return false;
    }
    //
    if ($("input[name=symptome_id]").is(":checked") && ($("input[name=symptome_id]:checked").length == 0 ||  $("input[name=symptome_id]:checked").length > 5)) {
        alert("Il faut entre 1 et 5 symptômes!");
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
        alert("Not working yet!");
        return;
        if (confirm("Etes-vous sûr?")) {

            $("#box_searching").show();
            $("#box_searching").html("Les notifications sont en cours d'envoie aux personnes concernées ...!");

            $.ajax({
                url: "/notifications/add",
                type: "POST",
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
            $("#searchname").val(ui.item.label); // display the selected text
            $("#personne_id_2").val(ui.item.value); // save selected id to hidden input
            if ($("#personne_id_2").val().trim() == "") {
                $("#new_personne").show();
            } else {
                $("#new_personne").hide();
            }
            return false;
        }
    });

    // change crp add contact
    $("#searchname").on("input propertychange change keyup paste", function() {
        if ($(this).val().trim() == "") {
            $("#personne_id_2").val("");
        }
        if ($(this).val().trim() == "" && $("#personne_id_2").val().trim() == "") {
            $("#personne_id_2").val("");
            $("#new_personne").show();
        } else if ($("#personne_id_2").val().trim() !== "") {
            $("#new_personne").hide();
        }
    });

    // in page personne vie condition
    $('#has_enfant').change(function() {
        if($(this).is(":checked")) {
            $("#exist_enfant").show();
        } else {
            $("#exist_enfant").hide();
        }
    });

    $('#has_personne_agee').change(function() {
        if($(this).is(":checked")) {
            $("#exist_personne_agee").show();
        } else {
            $("#exist_personne_agee").hide();
        }
    });

    $("#has_been_in_contact_personne_risque").change(function() {
        if($(this).is(":checked")) {
            $("#new_personne").show();
        } else {
            $("#new_personne").hide();
        }
    });

});