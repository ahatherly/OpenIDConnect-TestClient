"""
Flask app for testing the OpenID Connect extension.
"""
from flask import Flask, redirect
#from flask.ext.oidc import OpenIDConnect
#from flask_oidc import OpenIDConnect
from flask_oidc import OpenIDConnect

import json

import logging
logging.basicConfig()

config = { 'OIDC_CLIENT_SECRETS': './client_secrets.json',
           'OIDC_ID_TOKEN_COOKIE_SECURE': False,
           'OIDC_VALID_ISSUERS': 'http://localhost:8080/auth/realms/Test',
           'SECRET_KEY': 'web'};
oidc_overrides = {}

app = Flask(__name__)
app.config.update(config)
oidc = OpenIDConnect(app, **oidc_overrides)

"""
def index():
    return "too many secrets", 200, {
        'Content-Type': 'text/plain; charset=utf-8'
    }
"""

@app.route('/userinfo')
@oidc.accept_token()
def my_api():
    #return json.dumps('Welcome %s' % oidc.oidc_token_info['sub'])
    return json.dumps(oidc._retrieve_userinfo())

@app.route('/')
def index():
    if oidc.user_loggedin:
        return 'Welcome %s.<br/><a href="/userinfo">Click here to view the userinfo</a><br/><a href="/logout">Click here to log out</a>' % oidc.user_getfield('email')
    else:
        return 'Not logged in.</br><a href="/login">Click here to log in</a>'

@app.route('/login')
@oidc.require_login
def login():
    #return 'Welcome %s, your auth token contains:' % oidc.user_getfield('email')
    return redirect("/", code=302)

@app.route('/logout')
def logout():
    oidc.logout()
    return 'Logged out.</br><a href="/login">Click here to log in</a>'

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)