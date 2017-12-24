$( document ).ready(function() {
	
    function getCsrf() {
    	return $('input[name=csrfmiddlewaretoken]').val();
    }
    
    function getCalculationId() {
    	var url = window.location.href;
    	var id = url.substring(url.lastIndexOf('/') + 1);
    	return '/activities/calculation/' + id;
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCsrf());
            }
        }
    });
	
	$.ajax({
	    url: getCalculationId(),
	    type: 'GET',
	    beforeSend: function(xhr, settings) {
	      $.ajaxSettings.beforeSend(xhr, settings);
	    },
	    success: function(data) {
	    	var myCircle = Circles.create({
	    		id: 'circles-1',
	    		radius: 60,
	    		value: data.performance,
	    		maxValue: 100,
	    		width: 10,
	    		text: function(value){return value + '%';},
	    		colors: ['#D3B6C6', '#4B253A'],
	    		duration: 400,
	    		wrpClass: 'circles-wrp',
	    		textClass: 'circles-text',
	    		valueStrokeClass: 'circles-valueStroke',
	    		maxValueStrokeClass: 'circles-maxValueStroke',
	    		styleWrapper: true,
	    		styleText: true
    		});
	    	
	    	$('p').html('Potential achievements attained as a group');
	    },
	    error: function (request, status, error) {
	    	console.log('error');
	    }
	});
});