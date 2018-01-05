$( document ).ready(function() {
	
    function getCsrf() {
    	return $('input[name=csrfmiddlewaretoken]').val();
    }
    
    function getCalculationId() {
    	var url = window.location.href;
    	var id = url.substring(url.lastIndexOf('/') + 1);
    	return '/activities/calculation/' + id;
    }
    
    $('#copy-url-btn').on('click', function() {
    	var copyText = document.getElementById("copy-url");
    	copyText.select();
	    document.execCommand("Copy");
	    alert('The link has been copied to your clipboard, now share it with your friends on Strava!');
    });

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
	    		radius: 90,
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
	    		styleWrapper: false,
	    		styleText: true
    		});
	    	
	    	$.each(data.results, function(index, athlete) {
	    		$('#individuals').append(
				'<div class="card">'+
					'<div class="card-body">'+
						'<div class="row">'+
							'<div class="col-md-4">'+
								'<img src="'+ athlete.profile +'" alt="..." class="rounded-circle mx-auto margin" width="100">'+
							'</div>'+
							'<div class="col-md-8">'+
							    '<h5 class="card-title">'+ athlete.athlete +'</h5>'+
							    '<h6 class="card-subtitle mb-2 text-muted">Attained '+ athlete.achievements +' achievements</h6>'+
							    '<a href="#" class="card-link">View Activity</a>'+
						    '</div>'+
					    '</div>'+
				    '</div>'+	    
	  			'</div>'				    
			    );    		
	    	});
	    	
	    	$('h1').append(data.activity.name);
	    	$('#potential').append(data.achievement_potential);
	    	$('#distance').append(data.activity.distance);
	    	$('#activity-type').append(data.activity.type);
	    	$('#elevation').append(data.activity.elevation_gain);
	    	$('#copy-url').val(window.location.href);
	    },
	    error: function (request, status, error) {
	    	console.log('error');
	    }
	});
});