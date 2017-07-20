$(document).ready(function(c) {
	$('.alert-close').on('click', function(c){
		$('.message').fadeOut('slow', function(c){
	  		$('.message').remove();
		});
	});	  

    var submit_form = function(e) {
      	$.post($SCRIPT_ROOT + '/login', {
        	email: $('input[name="email"]').val(),
        	password: $('input[name="password"]').val(),
      	}, function(data) {
        	if("email" in data) {
        		$("#sh1").text(data.username)
        	}
        	if("password" in data) {
        		$("#sh3").text(data.password)
        	}
        	$('input[name="email"]').focus().select();
        	if("success" in data) {
        		window.location.href = "/detail?username=" + data.success
        	}
      	});
      	return false;
    };

    $('#submitBut').bind('click', submit_form);

    $('input[name="email"]').bind("click", function() {
        $('input[name="email"]').val("")
        $("#sh1").text("")
    })
    $('input[name="password"]').bind("click", function() {
        $('input[name="password"]').val("")
        $("#sh3").text("")
    })   

  
});