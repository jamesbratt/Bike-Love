from django.http import HttpResponse
from django.conf import settings
import requests
import json

class StravaApi():

    def Oauth(self, code):
        payload = {'client_id':settings.CLIENT_ID, 'client_secret':settings.CLIENT_SECRET, 'code':code}
        getStravaUser = requests.post(settings.OAUTH_URL, verify=False, data=payload)
        response = getStravaUser
        if response.status_code is not 200:
            raise ValueError(response.json()['message'])
        return response

    def Activities(self, token):
        headers = {'Authorization':'Bearer ' + token}
        getActivities = requests.get(settings.API_URL + 'athlete/activities', verify=False, headers=headers)
        response = getActivities
        if response.status_code is not 200:
            raise ValueError(response.json()['message'])
        return response
    
    def Activity(self, token, activity_id):
        headers = {'Authorization':'Bearer ' + token}
        getActivity = requests.get(settings.API_URL + 'activities/' + str(activity_id) + '/?include_all_efforts=true', verify=False, headers=headers)
        response = getActivity
        if response.status_code is not 200:
            raise ValueError(response.json()['message'])
        return response
    
    def related_activities(self, token, activity_id):
        headers = {'Authorization':'Bearer ' + token}
        get_related = requests.get(settings.API_URL + 'activities/' + str(activity_id) + '/related', verify=False, headers=headers)
        response = get_related
        if response.status_code is not 200:
            raise ValueError(response.json()['message'])
        return response
