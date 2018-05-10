# -*- coding: utf-8 -*-
from flask import Flask, render_template, abort
from .models import SearchResult, Word

app = Flask(__name__)


@app.route("/")
def index_view():
    results = SearchResult.select()
    return render_template('index.html', results=results)


@app.route("/words/")
def words_view():
    words = Word.select()
    return render_template('words.html', words=words)


@app.route("/words/<string:word_text>")
def word_view(word_text):
    try:
        word = Word.get(text=word_text)
    except Word.DoesNotExist:
        abort(404)
    return render_template('word.html', results=word.results, word_text=word_text)

