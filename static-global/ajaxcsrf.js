function getCsrf() {
	return $('input[name=csrfmiddlewaretoken]').val();
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", getCsrf());
        }
    }
});