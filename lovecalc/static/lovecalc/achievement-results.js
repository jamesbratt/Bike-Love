var map;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    zoom: 8
  });
}

$( document ).ready(function() {
	
	if(Cookies.get('feedback') !== 'true') {
		$('#interested').removeClass('invisible');
	}
    
    function getCalculationId() {
    	var url = window.location.href;
    	var id = url.substring(url.lastIndexOf('/') + 1);
    	return '/activities/calculation/' + id;
    }
    
    function zoomToObject(obj){
        var bounds = new google.maps.LatLngBounds();
        var points = obj.getPath().getArray();
        for (var n = 0; n < points.length ; n++){
            bounds.extend(points[n]);
        }
        map.fitBounds(bounds);
    }
    
    $('#copy-url-btn').on('click', function() {
    	var copyText = document.getElementById("copy-url");
    	copyText.select();
	    document.execCommand("Copy");
	    alert('The link has been copied to your clipboard, now share it with your friends on Strava!');
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
	    	
	    	var route = google.maps.geometry.encoding.decodePath(data.activity.route);
	    	console.log(route);
	        var line = new google.maps.Polyline({
	            path: route,
	            geodesic: true,
	            strokeColor: '#FF0000',
	            strokeOpacity: 1.0,
	            strokeWeight: 2
	          });

	        line.setMap(map);
	        zoomToObject(line);
	    	
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
							    '<a target="_blank" href="https://www.strava.com/activities/'+ athlete.activity_id +'" class="card-link">View Activity</a>'+
						    '</div>'+
					    '</div>'+
				    '</div>'+	    
	  			'</div>'				    
			    );    		
	    	});
	    	
	    	$('h1').append(data.activity.name);
	    	$('#potential').append(data.achievement_potential);
	    	$('#distance').append(((data.activity.distance/1000).toFixed(1)) + ' km / ' + (data.activity.distance/1609).toFixed(1) + ' mi');
	    	$('#activity-type').append(data.activity.type);
	    	$('#elevation').append(data.activity.elevation_gain + ' m');
	    	$('#copy-url').val(window.location.href);
	    },
	    error: function (request, status, error) {
	    	console.log('error');
	    }
	});
	
    $('.feedback').on('click', function(e) {
    	var feedback = false;
    	var answer = e.target.innerHTML;
    	if(answer === 'Yes!') {
    		feedback = true;
    	}
    	$.ajax({
    	    url: '/feedback/',
    	    type: 'POST',
    	    data: {feedback:feedback},
    	    dataType: 'json',
    	    beforeSend: function(xhr, settings) {
    	      $.ajaxSettings.beforeSend(xhr, settings);
    	    },
    	    success: function(data) {
    	    	Cookies.set('feedback', 'true');
    	    	$('#interested').addClass('invisible');
    	    	$('#feedbackSuccess').modal('show');
    	    },
    	    error: function (request, status, error) {
    	    	alert('Error!');
    	    }
    	});
    });
});