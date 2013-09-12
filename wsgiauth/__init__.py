from werkzeug.wrappers import Request
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound


class WSGIAuthMiddleware(object):
    def __init__(self, app, strategies=None, path_prefix="/auth"):
        self.app = app
        self.strategies = {} or strategies
        self.path_prefix = path_prefix

    def __call__(self, environ, start_response):
        request = Request(environ)
        if request.path.startswith(self.path_prefix):
            url_map = Map([
                Rule(self.path_prefix+'/<string:strategy>/', 
                     endpoint='request'),
                Rule(self.path_prefix+'/<string:strategy>/callback/', 
                     endpoint='callback'),
            ])

            try:
                endpoint, args = url_map.bind_to_environ(environ).match()

                if endpoint == 'request':
                    return self._request_phase(request, **args)(environ, start_response)
                elif endpoint == 'callback':
                    environ['wsgiauth'] = self._callback_phase(request, **args)
            except HTTPException as e:
                return e(environ, start_response)

        return self.app(environ, start_response)

    def _request_phase(self, request, strategy):
        try:
            _strategy = self.strategies[strategy]
        except KeyError:
            raise NotFound()
        return _strategy.request_phase(request)

    def _callback_phase(self, request, strategy):
        try:
            _strategy = self.strategies[strategy]
        except KeyError:
            raise NotFound()
        return _strategy.callback_phase(request)
