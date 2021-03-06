from api import API
from middleware import Middleware

app = API()
# app()


@app.route("/home")
def home(request, response):
    response.text = "Hello from HOME page"


@app.route("/about")
def about(request, response):
    response.text = "Hello from ABOUT page"


@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"


@app.route("/sum/{num_1:d}/{num_2:d}")
def sum(request, response, num_1, num_2):
    total = int(num_1) + int(num_2)
    response.text = f"{num_1} + {num_2} = {total}"


@app.route("/book")
class BooksResource:
    def get(self, request, response):
        response.text = "Books page"

    def post(self, request, response):
        response.text = "Endpoint to create a book"


def handler(req, resp):
    resp.text = "sample"


app.add_route("/sample", handler)


def custom_exception_handler(req, resp, exception_cls):
    resp.text = str(exception_cls)


app.add_exception_handler(custom_exception_handler)


@app.route("/exception")
def exception_throwing_handler(request, response):
    raise AssertionError("This handler should not be used.")


class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Processing request ", req.url)

    def process_response(self, req, resp):
        print("Processing response", req.url)


app.add_middleware(SimpleCustomMiddleware)


@app.route("/template")
def template_handler(req, resp):
    resp.html = app.templates("index.html", context={"name": "Bumbo", "title": "Best Framework"})


@app.route("/json")
def json_handler(req, resp):
    resp.json = {"name": "data", "type": "JSON"}


@app.route("/text")
def text_handler(req, resp):
    resp.text = "This is a simple text"
