from django.http import JsonResponse
from django.views.generic import View

from .models import GoalFeedback

class SendFeedback(View):

    def post(self, request, **kwargs):
        if request.is_ajax():
            feedback = False
            feedback_result = request.POST.get("feedback")
            if feedback_result == 'true':
                feedback = True
            try:
                results = GoalFeedback.objects.create(feedback=feedback)
            except:
                response = JsonResponse(
                    {
                        'status':'false',
                        'message':'Sorry, there was a problem. Please refresh the page and try again.'
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
