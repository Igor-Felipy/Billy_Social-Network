from app import app
from flask import render_template


@app.route("/index/")
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login/")
def login():
    return render_template('base.html')