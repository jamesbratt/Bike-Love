from django.http import HttpResponse
from django.conf import settings
import requests
import json

class StravaApi():

    def Oauth(self, code):
        payload = {'client_id':settings.CLIENT_ID, 'client_secret':settings.CLIENT_SECRET, 'code':code}
        getStravaUser = requests.post(settings.OAUTH_URL, verify=False, data=payload)
        response = getStravaUser
        return response

    def Activities(self, token):
        headers = {'Authorization':'Bearer ' + token}
        getActivities = requests.get(settings.API_URL + 'athlete/activities', verify=False, headers=headers)
        response = getActivities
        print(response)
        return response
