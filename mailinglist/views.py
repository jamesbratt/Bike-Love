from django.http import JsonResponse
from django.views.generic import View

from .models import Subscriber

class Subscribe(View):

    def post(self, request, **kwargs):
        if request.is_ajax():

            email_address = request.POST.get("email")

            try:
                results = Subscriber.objects.create(email=email_address)
            except:
                response = JsonResponse(
                    {
                        'status':'false',
                    }
                )
                response.status_code = 500
                return response

            response = JsonResponse(
                {
                    'status':'true',
                }
            )
            response.status_code = 200
            return response
