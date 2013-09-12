from werkzeug.utils import redirect


class GitHub(object):
    def __init__(self, client_id, client_secret):
        pass

    def request_phase(self, request):
        return redirect('/auth/github/callback')

    def callback_phase(self, request):
        return None