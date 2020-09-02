from app import app

@app.route("/index")
@app.route("/")
def index():
    return "Hello World!"


@app.route("/teste/", defaults={'name':None})
@app.route("/teste/<name>")
def teste(name):
    if name:
        return "Olá, %s!" % name
    else:
        return "Olá, Usuario!"