import json

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

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
    
    
class CalculateTheLove(StravaTokenCheckMixin, View):

    def get(self, request **kwargs):
        
        # Get the activity id
        
        # Get the full activity (dates required)
        
        # Extract every segment id for each segment effort for the activity 
        
        # Make a request for the related activities
        
        # Extract the athlete details from each related activity
        
        # Now for every athlete, loop over each segment id
        
        # And make a segment effort request filtered by the athlete/activity date range
        
        # This should yield a segment effort id for every segment in the activity for each athlete in the group
        
        # Now for every athletes segment efforts make a request for that effort stream
        
        """
        {
            segment1: [
                {athlete: 1, effort_id: 10, data: []},
                {athlete: 2, effort_id: 23, data: []},
            ],
            segment2: [
                {athlete: 1, effort_id: 45, data: []},
                {athlete: 2, effort_id: 76, data: []},
            ],
        }
        """
        
        # Now use Pythons zip tool to iterate over each effort in each segment
        # And calculate the average distance between each athlete at each data point 
        return HttpResponseRedirect('/')
