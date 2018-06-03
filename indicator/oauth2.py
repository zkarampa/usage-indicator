#!/usr/bin/env python3.3.
import base64

import requests
from six.moves.urllib.parse import quote, parse_qs


class OAuth2Error(Exception):
    pass


class ConfigurationError(OAuth2Error):
    pass


class Oauth2(object):
    client_id = None
    client_secret = None
    site = None
    redirect_uri = None
    authorization_url = '/oauth/authorize'
    token_url = '/oauth/token'
    scope_sep = None

    def __init__(self, client_id=None, client_secret=None, site=None,
                 redirect_uri=None, authorization_url=None,
                 token_url=None, scope_sep=None):
        """
        Initializes the hook with OAuth2 parameters
        """
        if client_id is not None:
            self.client_id = client_id
        if client_secret is not None:
            self.client_secret = client_secret
        if site is not None:
            self.site = site
        if redirect_uri is not None:
            self.redirect_uri = redirect_uri
        if authorization_url is not None:
            self.authorization_url = authorization_url
        if token_url is not None:
            self.token_url = token_url
        if scope_sep is not None:
            self.scope_sep = scope_sep

    def _check_configuration(self, *attrs):
        for attr in attrs:
            if getattr(self, attr, None) is None:
                raise ConfigurationError("{} not configured".format(attr))

    def get_token_password_credentials(self, username, password, scope):
        self._check_configuration("site", "token_url",
                                  "client_id", "client_secret")
        if isinstance(scope, (list, tuple, set, frozenset)):
            self._check_configuration("scope_sep")
            scope = self.scope_sep.join(scope)

        url = "%s%s" % (self.site, quote(self.token_url))
        data = {
            "grant_type": "password",
            "password": password,
            "username": username,
            "scope": scope
        }

        auth = self.client_id + ":" + self.client_secret
        headers = {
            "Authorization": "Basic {}".format(bytes.decode(base64.b64encode(bytes(auth, "utf-8"))))
        }
        return self._make_request(url, data=data, headers=headers)

    def _make_request(self, url, **kwargs):
        response = requests.post(url, **kwargs)
        try:
            return response.json()
        except ValueError:
            pass
        return parse_qs(response.content)
