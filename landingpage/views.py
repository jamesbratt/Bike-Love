from django.http import HttpResponseRedirect
from django.views.generic import View

class Logout(View):

    def get(self, request, **kwargs):
        
        if 'token' in request.session:
            del request.session['token']
            del request.session['athlete']
            
        return HttpResponseRedirect('/')
