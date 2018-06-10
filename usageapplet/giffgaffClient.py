from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session


class GiffgaffClient:
    token_url = "https://id.giffgaff.com/auth/oauth/token"
    profile_url = "https://publicapi.giffgaff.com/giffgaff-api/profile.json"
    client_id = "app_android"
    client_secret = "axicnbYM64SkKMgXdkRlwMrZ7DrVdrZg6voM9uOqcfQ="

    def __init__(self, username, password):
        self.oauth = OAuth2Session(client=LegacyApplicationClient(client_id=GiffgaffClient.client_id))
        self.oauth.fetch_token(
            token_url=GiffgaffClient.token_url,
            username=username,
            password=password,
            client_id=GiffgaffClient.client_id,
            client_secret=GiffgaffClient.client_secret
        )
        self.username = username
        self.password = password

    def get_data_allowance(self):
        profile = self.oauth.request(url=GiffgaffClient.profile_url, method='GET').json()

        data_left = profile['current_goodybag']['data_left']
        data_max = profile['current_goodybag']['data_max']

        # data_left_amount = profile.json()['current_goodybag']['data_left_amount']
        # data_max_amount = profile.json()['current_goodybag']['data_max_amount']

        return {
            "max": data_max,
            "left": data_left
        }
