# -*- coding: utf-8 -*-
import datetime
from flask import Flask, render_template, abort
from peewee import fn
from .models import SearchResult, Word

app = Flask(__name__)


@app.route("/")
def index_view():
    today = datetime.date.today()
    results = SearchResult.select().where(SearchResult.stored_at == today)
    return render_template('index.html', results=results)


@app.route("/word/")
def word_list_view():
    words = Word.select()
    return render_template('words.html', words=words)


@app.route("/word/<string:word_text>")
def word_view(word_text):
    try:
        word = Word.get(text=word_text)
    except Word.DoesNotExist:
        abort(404)
    return render_template('word.html', results=word.results, word_text=word_text)


@app.route("/date/")
def date_list_view():
    query = SearchResult.select(fn.Distinct(SearchResult.stored_at))
    dates = [r.stored_at for r in query]
    return render_template('dates.html', dates=dates)


@app.route("/date/<string:date_text>")
def date_view(date_text):
    date = datetime.datetime.strptime(date_text, "%Y-%m-%d").date()
    results = SearchResult.select().where(SearchResult.stored_at == date)
    return render_template('date.html', results=results, date_text=date_text)
