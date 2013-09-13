from werkzeug.utils import redirect
from werkzeug.urls import url_encode

import requests


class OAuth2(object):
    authorize_url = None
    access_token_url = None
    api_url = None

    def __init__(self, client_id, client_secret):
        if self.authorize_url is None:
            raise NotImplementedError
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