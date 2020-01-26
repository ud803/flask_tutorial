from flask import Flask, g, request, Response, make_response, session
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.debug = True

app.config.update(
    SECRET_KEY='X1234',
    SESSION_COOKIE_NAME='pyweb_flask_session',
    PERMANENT_SESSION_LIFETIME=timedelta(31)
)

# Logout
@app.route("/delsess")
def delsess():
    if session.get("Token"):
        del session["Token"]
    return "Session이 삭제되었습니다!"

@app.route("/wc")
def wc():
    key = request.values.get('key', None)
    val = request.values.get('val', None)
    res = Response("SET COOKIE")
    res.set_cookie(key, val)
    session["Token"] = "123X"
    return make_response(res)

@app.route("/rc")
def rc():
    key = request.values.get('key', None)
    val = request.cookies.get(key)
    return "cookie[{}] = {}, {}".format(key, val, session.get("Token"))


@app.route("/")
def hello_world():
    return "Hello Flask World~!##"


