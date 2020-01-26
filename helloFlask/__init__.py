from flask import Flask, g, Response, make_response

app = Flask(__name__)
app.debug = True

@app.route("/res1")
def res1():
    custom_res = Response("Custom Response", 200, {'test' : 'ttt'})
    return make_response(custom_res)

@app.route("/test_wsgi")
def wsgi_test():
    def application(environ, start_response):
        body = "The request method was {}".format(environ["REQUEST_METHOD"])
        headers = [ ('Content-Type', 'text/plain'),
                    ('Content-Length', str(len(body)))]
        start_response('200 OK', headers)
        return [body]

    return make_response(application)


# @app.before_request
# def before_request():
#     print("before_request!!!")
#     g.str = "한글!!"
    

# @app.route("/gg")
# def hello_world():
#     return "Hello Flask World" + getattr(g, "str", "111")

@app.route("/")
def hello_world2():
    return "Hello Flask World~!##"


