import json

from django.http import HttpResponseRedirect, Http404
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.views.generic import View

from strava.views import StravaApi
from .models import LoveCalculation


class StravaTokenCheckMixin(object):
    
    def dispatch(self, request, *args, **kwargs):

        code = request.GET.get('code', '')

        if 'token' not in request.session:
            if code is not '':
                try:
                    stravaResponse = StravaApi().Oauth(str(code))
                except ValueError as e:
                    return HttpResponse(e)

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

    def dispatch(self, request, *args, **kwargs):
        try:
            LoveCalculation.objects.get(pk=self.kwargs['calculation_id'])
        except LoveCalculation.DoesNotExist:
            raise Http404

        return super(AchievementResultsView, self).dispatch(request, *args, **kwargs)
    

class FetchCalculation(View):

    def get(self, request, **kwargs):
        if request.is_ajax():
            try:
                results = LoveCalculation.objects.get(pk=self.kwargs['calculation_id'])
            except LoveCalculation.DoesNotExist:
                response = JsonResponse(
                    {
                        'status':'false',
                        'message':'There was a problem processing this activity.'
                    }
                )
                response.status_code = 500
                return response

            return JsonResponse(results.results)
    
    
class CalculateTheLove(StravaTokenCheckMixin, View):

    def get(self, request, **kwargs):
        
        calculation_activity_id = None
        
        calculation = LoveCalculation.objects.filter(activity_id=self.kwargs['activity_id'])
        
        if calculation.count() > 0:
            calculation_activity_id = str(calculation[0].id)
        else:
            token = self.request.session.get('token')

            try:
                activity = StravaApi().Activity(str(token), self.kwargs['activity_id'])
            except ValueError as e:
                return HttpResponse(e)
            
            activityObj = activity.json()
            
            if activityObj['athlete']['id'] != self.request.session.get('athlete')['id']:
                return HttpResponse('Not your activity')
            
            try:
                related_activities = StravaApi().related_activities(str(token), self.kwargs['activity_id'])
            except ValueError as e:
                return HttpResponse(e)
            
            achievements = []
            base_activity = {
                'name': activityObj['name'],
                'distance': activityObj['distance'],
                'elevation_gain': activityObj['total_elevation_gain'],
                'type': activityObj['type'],
                'route': activityObj['map']['polyline'],
                'athlete': self.request.session.get('athlete')['firstname'],
            }
            
            total_segments = len(activityObj['segment_efforts']) * (len(related_activities.json()) + 1)
            
            achievements.append(
                {
                    'athlete': self.request.session.get('athlete')['firstname'],
                    'achievements': activityObj['achievement_count'],
                    'activity_id': activityObj['id']
                }
            )
            
            for activity in related_activities.json():
                obj = {
                    'athlete': activity['athlete']['firstname'],
                    'achievements': activity['achievement_count'],
                    'activity_id': activity['id']
                }
                achievements.append(obj)
                
            achievement_sum = sum(achievement['achievements'] for achievement in achievements)
            performance = round(achievement_sum/total_segments * 100, 0)
                
            results = {
                'results': achievements,
                'achievement_potential': total_segments,
                'performance': int(performance),
                'activity': base_activity
            }
            
            new_calculation = LoveCalculation.objects.create(
                activity_id=int(activityObj['id']),
                results=results
            )
            
            calculation_activity_id = str(new_calculation.id)
                
        return HttpResponseRedirect('/activities/results/' + calculation_activity_id)
