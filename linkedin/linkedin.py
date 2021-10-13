# -*- coding: utf-8 -*-
import hashlib
import json
import random
from collections import namedtuple
from urllib.parse import quote

import requests

AccessToken = namedtuple("AccessToken", ["access_token", "expires_in"])


class LinkedinOAuth2:
    AUTHORIZATION_URL = "https://www.linkedin.com/uas/oauth2/authorization"
    ACCESS_TOKEN_URL = "https://www.linkedin.com/uas/oauth2/accessToken"

    def __init__(self, key, secret, redirect_uri, permissions=None):
        self.key = key
        self.secret = secret
        self.redirect_uri = redirect_uri
        self.permissions = permissions or []
        self.state = None
        self.authorization_code = None
        self.token = None
        self._error = None

    @property
    def authorization_url(self):
        data = {
            "response_type": "code",
            "client_id": self.key,
            "scope": (" ".join(self.permissions)).strip(),
            "state": self.state or self._make_new_state(),
            "redirect_uri": self.redirect_uri,
        }
        params = [f"{quote(k)}={quote(v)}" for k, v in data.items()]
        return f"{self.AUTHORIZATION_URL}?{'&'.join(params)}"

    @property
    def last_error(self):
        return self._error

    def _make_new_state(self):
        return hashlib.md5(
            "{}{}".format(random.randrange(0, 2 ** 63), self.secret).encode("utf8")
        ).hexdigest()

    def get_access_token(self, timeout=60):
        if not self.authorization_code:
            raise Exception("You must first get the authorization code")

        data = {
            "grant_type": "authorization_code",
            "code": self.authorization_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.key,
            "client_secret": self.secret,
        }
        response = requests.post(self.ACCESS_TOKEN_URL, data=data, timeout=timeout)
        response.raise_for_status()
        response = response.json()
        self.token = AccessToken(response["access_token"], response["expires_in"])
        return self.token


class LinkedIn:
    BASE_URL = "https://api.linkedin.com"

    def __init__(self, authentication=None, token=None):
        if not (authentication or token):
            raise Exception("Either authentication instance or access token is required")
        self.authentication = authentication
        if not self.authentication:
            self.authentication = LinkedinOAuth2("", "", "")
            self.authentication.token = AccessToken(token, None)

    def make_request(self, method, url, data=None, params=None, headers=None, timeout=60):
        if headers is None:
            headers = {"X-Restli-Protocol-Version": "2.0.0", "Content-Type": "application/json"}
        else:
            headers.update(
                {"X-Restli-Protocol-Version": "2.0.0", "Content-Type": "application/json"}
            )

        if params is None:
            params = {}

        kw = dict(data=data, params=params, headers=headers, timeout=timeout)
        params.update({"oauth2_access_token": self.authentication.token.access_token})

        return requests.request(method.upper(), url, **kw)

    def create_ugc_post(
        self, author=None, text=None, lifecycle_state="PUBLISHED", visibility_code="PUBLIC"
    ):
        """
        Create UGC Post
        """
        data = {
            "author": author,
            "lifecycleState": lifecycle_state,
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": visibility_code},
        }
        url = f"{self.BASE_URL}/v2/ugcPosts"
        response = self.make_request("POST", url, data=json.dumps(data))
        return response.json()

    def get_profile(self):
        """
        Retrieve the current member's profile based on the access token.
        This API requires one of these permissions: r_liteprofile, r_basicprofile
        """
        url = f"{self.BASE_URL}/v2/me"
        response = self.make_request("GET", url)
        return response.json()

    def get_organization_acls(self):
        """
        Find a Member's Organization Access Control Information.
        This call requires member to be an "ADMINISTRATOR".
        """
        url = f"{self.BASE_URL}/v2/organizationalEntityAcls"
        params = {
            "q": "roleAssignee",
            "state": "APPROVED",
        }
        response = self.make_request("GET", url, params=params)
        return response.json()

    def get_organization(self, organization_id):
        """
        Retrieve an Administered Organization
        """
        url = f"{self.BASE_URL}/v2/organizations/{organization_id}"
        response = self.make_request("GET", url)
        return response.json()
