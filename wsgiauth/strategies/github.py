from werkzeug.utils import redirect
from werkzeug.urls import url_encode

import requests


class GitHub(object):
    authorize_url = 'https://github.com/login/oauth/authorize'
    access_token_url = 'https://github.com/login/oauth/access_token'
    api_url = 'https://api.github.com/user'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def request_phase(self, request, redirect_uri):
        url = '%s?%s' % (self.authorize_url, 
                         url_encode({
                            'client_id': self.client_id, 
                            'redirect_uri': redirect_uri,
                         }))
        return redirect(url)

    def callback_phase(self, request):
        code = request.args.get('code')
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
        }
        headers = {'Accept': 'application/json'}
        token_data = requests.post(self.access_token_url, data=data, headers=headers).json()
        if 'access_token' in token_data:
            return requests.get(self.api_url, params=token_data, headers=headers).json()
        return None