# -*- coding: utf-8 -*-
import datetime
from flask import Flask, render_template, abort
from peewee import fn
from .models import SearchResult, Word

app = Flask(__name__)


def deco(results, target_day):
    yesterday = target_day - datetime.timedelta(days=1)
    for r in results:
        try:
            yr = SearchResult.get(word=r.word, stored_at=yesterday)
            r.all_increase = r.num_of_all - yr.num_of_all
            r.safe_increase = r.num_of_safe - yr.num_of_safe
            r.r18_increase = r.num_of_r18 - yr.num_of_r18

            _r18_rate_increase = r.calc_r18_rate() - yr.calc_r18_rate()
            r.r18_rate_increase = "{:.2}".format(_r18_rate_increase)

        except SearchResult.DoesNotExist:
            pass
        yield r


@app.route("/")
def index_view():
    today = datetime.date.today()
    results = SearchResult.select().where(SearchResult.stored_at == today)

    return render_template("index.html", results=deco(results, today))


@app.route("/word/")
def word_list_view():
    words = Word.select()
    return render_template("words.html", words=words)


@app.route("/word/<string:word_text>")
def word_view(word_text):
    try:
        word = Word.get(text=word_text)
    except Word.DoesNotExist:
        abort(404)
    return render_template("word.html", results=word.results, word_text=word_text)


@app.route("/date/")
def date_list_view():
    query = SearchResult.select(fn.Distinct(SearchResult.stored_at))
    dates = [r.stored_at for r in query]
    return render_template("dates.html", dates=dates)


@app.route("/date/<string:date_text>")
def date_view(date_text):
    date = datetime.datetime.strptime(date_text, "%Y-%m-%d").date()
    results = SearchResult.select().where(SearchResult.stored_at == date)
    return render_template(
        "date.html", results=deco(results, date), date_text=date_text
    )
