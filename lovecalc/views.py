import json

from django.http import HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.views.generic import View

from strava.views import StravaApi


class StravaTokenCheckMixin(object):
    
    def dispatch(self, request, *args, **kwargs):

        code = request.GET.get('code', '')

        if 'token' not in request.session:
            if code is not '':
                try:
                    stravaResponse = StravaApi().Oauth(str(code))
                except:
                    return HttpResponseRedirect('/')

                stravaData = stravaResponse.json()
                request.session['token'] = stravaData['access_token']
                request.session['athlete'] = stravaData['athlete']
            else:
                return HttpResponseRedirect('/')

        return super(StravaTokenCheckMixin, self).dispatch(request, *args, **kwargs)


class ActivityListView(StravaTokenCheckMixin, TemplateView):
 
    template_name = 'lovecalc/activity-list.html'

    def get_context_data(self, **kwargs):
        context = super(ActivityListView, self).get_context_data(**kwargs)
        token = self.request.session.get('token')
        stravaData = StravaApi().Activities(str(token))
        activities = stravaData.json()
        
        group_activities = []
        
        for activity in activities:
            if activity['athlete_count'] > 1:
                group_activities.append(activity)

        context['group_activities'] = group_activities
        return context


class AchievementResultsView(TemplateView):
 
    template_name = 'lovecalc/achievement-results.html'

    def get_context_data(self, **kwargs):
        context = super(AchievementResultsView, self).get_context_data(**kwargs)
        return context
    

class FetchCalculation(View):

    def get(self, request, **kwargs):
        if request.is_ajax():
            return JsonResponse({})
    
    
class CalculateTheLove(StravaTokenCheckMixin, View):

    def get(self, request, **kwargs):
        
        token = self.request.session.get('token')
        activity = StravaApi().Activity(str(token), self.kwargs['activity_id'])
        activityObj = activity.json()
        
        related_activities = StravaApi().related_activities(str(token), self.kwargs['activity_id'])
        
        achievements = []
        
        total_segments = len(activityObj['segment_efforts']) * (len(related_activities.json()) + 1)
        
        achievements.append(
            {
                'athlete': self.request.session.get('athlete')['firstname'],
                'achievements': activityObj['achievement_count']
            }
        )
        
        for activity in related_activities.json():
            obj = {
                'athlete': activity['athlete']['firstname'],
                'achievements': activity['achievement_count']
            }
            achievements.append(obj)
            
        achievement_sum = sum(achievement['achievements'] for achievement in achievements)
        performance = round(achievement_sum/total_segments * 100, 0)
            
        results = [{'results': achievements, 'achievement_potential': total_segments, 'performance': int(performance)}]
            
        return HttpResponse(results)
