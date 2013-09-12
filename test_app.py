from wsgiauth import WSGIAuthMiddleware
from wsgiauth.strategies.github import GitHub

from werkzeug.serving import run_simple
from flask import Flask, request

app = Flask(__name__)

@app.route('/auth/github/callback/')
def github_callback():
    print request.environ
    return 'Hello GitHub user!'

if __name__ == '__main__':
    gh = GitHub(client_id="69e112615cb182eb32ca",
                client_secret="7d371355563bd125e926e430a080a7dd73dc923e")
    app = WSGIAuthMiddleware(app, strategies={'github': gh})
    run_simple('localhost', 5000, app,
               use_reloader=True, use_debugger=True, use_evalex=True)