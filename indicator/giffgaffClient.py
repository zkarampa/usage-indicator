import requests
from indicator.oauth2 import Oauth2


class GiffgaffClient(Oauth2):
    site = "https://id.giffgaff.com"
    token_url = "/auth/oauth/token"
    scope_sep = " "

    client_id = "app_android"
    client_secret = "axicnbYM64SkKMgXdkRlwMrZ7DrVdrZg6voM9uOqcfQ="

    access_token = None

    def __init__(self, username, password, scope):
        super(GiffgaffClient, self).__init__(
            client_id=self.client_id,
            client_secret=self.client_secret,
            site=self.site,
            token_url=self.token_url,
            scope_sep=self.scope_sep
        )

        data = self.get_token_password_credentials(username, password, scope)
        self.access_token = data.get("access_token")

    def get_profile(self):
        profile_url = 'https://publicapi.giffgaff.com/giffgaff-api/profile.json'
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer {}".format(self.access_token)
        }

        return requests.get(url=profile_url, headers=headers)
