from django.shortcuts import redirect
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from rest_framework import response
from rest_framework.decorators import api_view
import os


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

@api_view(('GET',))
def GoogleCalendarInitView(request):
        flow = InstalledAppFlow.from_client_secrets_file(
            'getEvents/client_secret.json',
            scopes=['https://www.googleapis.com/auth/calendar.events']
        )

        flow.redirect_uri = 'http://127.0.0.1:8000/rest/v1/calendar/redirect/'

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
        )
        request.session['state'] = state
        return redirect(authorization_url)


event_list = []
@api_view(('GET',))
def GoogleCalendarRedirectView(request):
        state = request.GET.get('state')
        flow = InstalledAppFlow.from_client_secrets_file(
            'getEvents/client_secret.json',
            scopes=['https://www.googleapis.com/auth/calendar.events'],
            state=state
        )
        flow.redirect_uri = 'http://127.0.0.1:8000/rest/v1/calendar/redirect/'
        authorization_response = request.build_absolute_uri()
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials

        request.session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        credentials = Credentials(
            **request.session['credentials']
        )
        service = build('calendar', 'v3', credentials=credentials)
        timeMin = '2023-01-01T00:00:00-07:00'

        # Call the Calendar API
        events_result = service.events().list(calendarId='primary', timeMin=timeMin,
                                              maxResults=20, singleEvents=True, orderBy='startTime').execute()
        for event in events_result['items']:
            event_list.append(event)

        return response.Response({"events":event_list})
