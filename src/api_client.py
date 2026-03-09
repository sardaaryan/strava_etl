import os
import requests
from dotenv import load_dotenv

load_dotenv()

class StravaClient:
    def __init__(self):
        self.client_id = os.getenv('STRAVA_CLIENT_ID')
        self.client_secret = os.getenv('STRAVA_CLIENT_SECRET')
        self.refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')
        self.access_token = self._refresh_access_token()

    def _refresh_access_token(self):
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }
        res = requests.post('https://www.strava.com/oauth/token', data=payload)
        res.raise_for_status()
        return res.json()['access_token']

    def get_activities(self, per_page=30):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = f"https://www.strava.com/api/v3/athlete/activities?per_page={per_page}"
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        return res.json()