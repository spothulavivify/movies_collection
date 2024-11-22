import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.conf import settings

class MovieService:
    def __init__(self):
        self.base_url = settings.MOVIE_API_URL
        self.auth = (settings.MOVIE_API_USERNAME, settings.MOVIE_API_PASSWORD)
        self.session = self._create_session()

    def _create_session(self):
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def get_movies(self, page=1):
        try:
            response = self.session.get(
                self.base_url,
                params={'page': page},
                auth=self.auth,
                timeout=5,
                verify=False
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching movies: {str(e)}")