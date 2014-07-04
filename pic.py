#!/usr/bin/env python2.7
# coding: utf-8
# author: sandtears
# e-mail: me@sandtears.com

from flask import Flask, request, make_response, render_template
from flask import url_for, redirect
import config
import httplib
import requests
import json


app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('pic'))


@app.route('/oauth.html')
def oauth():
    if not (config.client_id and config.redirect_uri):
        return 'Error: No client_id or redirect_uri'
    else:
        url = 'https://api.weibo.com/oauth2/authorize?client_id=%s&response_type=code&redirect_uri=%s'\
              % (config.client_id, config.redirect_uri)
        return '<script>window.location.href="%s"</script>' % url


def get_access_token(code):
    url = "/oauth2/access_token?client_id=%s" % config.client_id + \
          "&client_secret=%s" % config.client_secret + \
          "&grant_type=authorization_code&redirect_uri=%s" % config.redirect_uri + \
          "&code=%s" % code
    conn = httplib.HTTPSConnection("api.weibo.com")
    conn.request("POST", url)
    resp = conn.getresponse().read()
    result = json.loads(resp)
    conn.close()
    if result.get('error'):
        return 'Error: %s' % result['error']
    else:
        token = result['access_token']
        return "Your access_token is <code>%s</code>" % token


@app.route('/access_token.html')
def access_token():
    code = request.args.get('code', '')
    if not code:
        return 'Error: No code...'
    else:
        return get_access_token(code)


@app.route('/login.html', methods=["GET", "POST"])
def login():
    if request.cookies.get('password') == config.password:
        return redirect(url_for('pic'))
    if request.method == 'GET':
        return render_template('login.html')
    else:
        password = request.form['password']
        if password != config.password:
            return render_template('login.html', messages=["Error Password..."])
        else:
            resp = make_response(redirect(url_for('pic')))
            resp.set_cookie('password', password)
            return resp

        
@app.route('/pic.html', methods=["GET", "POST"])
def pic():
    if request.cookies.get('password') != config.password:
        return redirect(url_for("login"))
    if not config.access_token:
        return redirect(url_for("oauth"))
    if request.method == 'GET':
        return render_template('pic.html')
    else:
        f = request.files['pic']
        data = config.params
        url = "https://upload.api.weibo.com/2/statuses/upload.json"
        req = requests.post(url, data=data, files={'pic': f})
        resp = req.text
        result = json.loads(resp)
        if result.get('error'):
            return result['error']
        else:
            return render_template('result.html', pic=result['original_pic'])

if __name__ == '__main__':
    app.run()