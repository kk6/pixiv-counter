# -*- coding: utf-8 -*-
from flask import Flask, render_template
from .models import SearchResult

app = Flask(__name__)


@app.route("/")
def hello():
    results = SearchResult.select()
    return render_template('index.html', results=results)
