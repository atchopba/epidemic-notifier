$(document).ready(function(){

	// bouton rechercher
	$("#btnsearch").click(function() {

        search_text = $("#search_text").val().trim();

        if (search_text == "" ) {
            alert("Renseigner le libellé et la ville, s'il vous plait !");
            return;
        }

        $("#boxresult").css("display", "none");
        $("#boxloading").css("display", "block");

    	$.ajax({
    		url: "/search",
    		type: "POST",
    		data: {
    			q: search_text
    		},
    		success : function(data) {
    			tweets = JSON.parse(data);
    			console.log(tweets);
    			_html = "";
    			if (tweets && tweets.length > 0) {
        			tweets.forEach(function(t) {
            			_html += "<tr><td>"+ t[0] +"</td><td>"+ t[1] +"</td><td>"+ t[2] +"</td><td>"+ t[3] +"</td><td>"+ t[4] +"</td><td>"+ t[5] +"</td><td>"+ t[6] +"</td></tr>";
        			});
    			} else {
        			_html = "<tr><td colspan='7'>No results!</td></tr>";
    			}
    			//
        		$("#boxloading").css("display", "none");
    			$("#boxresult").css("display", "block");
    			$(".tbody_result").html(_html);
    		},
    		error: function(result, status, error) {
        		$("#boxloading").css("display", "none");
				alert("Une erreur est survenue. Veuillez ressayer!");
			}
    	});

  	});

});