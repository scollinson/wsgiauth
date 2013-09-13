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
                     endpoint=self._request_phase),
                Rule(self.path_prefix+'/<string:strategy>/callback/', 
                     endpoint=self._callback_phase),
            ])

            try:
                endpoint, args = url_map.bind_to_environ(environ).match()
                return endpoint(environ, start_response, request, **args)
            except HTTPException as e:
                return e(environ, start_response)

        return self.app(environ, start_response)

    def _request_phase(self, environ, start_response, request, strategy):
        _strategy = self.strategies.get(strategy)
        if _strategy is None:
            raise NotFound()
        redirect_uri = '%s://%s%s/%s/callback/' % (request.scheme, request.host, self.path_prefix, strategy)
        return _strategy.request_phase(request, 
                                       redirect_uri)(environ, start_response)

    def _callback_phase(self, environ, start_response, request, strategy):
        _strategy = self.strategies.get(strategy)
        if _strategy is None:
            raise NotFound()
        environ['wsgiauth'] = _strategy.callback_phase(request)
        return self.app(environ, start_response)
