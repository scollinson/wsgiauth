from .oauth2 import OAuth2


class GitHub(OAuth2):
    authorize_url = 'https://github.com/login/oauth/authorize'
    access_token_url = 'https://github.com/login/oauth/access_token'
    api_url = 'https://api.github.com/user'