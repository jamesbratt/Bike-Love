$( document ).ready(function() {
    $('.signup').on('click', function(e) {
    	e.preventDefault();
    	var email = $('.signupemail').val();
    	if(email === '' || email === undefined || email === null) {
    		alert('Please enter a valid email address');
    	} else {
        	$.ajax({
        	    url: '/subscribe/',
        	    type: 'POST',
        	    data: {email:email},
        	    dataType: 'json',
        	    beforeSend: function(xhr, settings) {
        	      $.ajaxSettings.beforeSend(xhr, settings);
        	    },
        	    success: function(data) {
        	    	alert('You have successfully signed up to the Superchamp newsletter!');
        	    },
        	    error: function (request, status, error) {
        	    	alert('Error!');
        	    }
        	});    		
    	}
    });

    $('.modalsignup').on('click', function(e) {
    	e.preventDefault();
    	var email = $('.modalsignupemail').val();
    	if(email === '' || email === undefined || email === null) {
    		alert('Please enter a valid email address');
    	} else {
        	$.ajax({
        	    url: '/subscribe/',
        	    type: 'POST',
        	    data: {email:email},
        	    dataType: 'json',
        	    beforeSend: function(xhr, settings) {
        	      $.ajaxSettings.beforeSend(xhr, settings);
        	    },
        	    success: function(data) {
        	    	alert('You have successfully signed up to the Superchamp newsletter!');
        	    	$('#feedbackSuccess').modal('hide');
        	    },
        	    error: function (request, status, error) {
        	    	alert('Error!');
        	    }
        	});    		
    	}
    });
});