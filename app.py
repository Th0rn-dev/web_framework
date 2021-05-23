from api import API

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


@app.route("/template")
def template_handler(req, resp):
    resp.body = app.templates(
        "index.html", context={"name": "Bumbo", "title": "Best Framework"}
    ).encode()
