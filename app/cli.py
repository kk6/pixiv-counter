# -*- coding: utf-8 -*-
from datetime import date
import time

import click

from crawler import PixivCrawler
from models import Word, SearchResult


@click.command()
@click.argument("pixiv_id")
@click.argument("password")
@click.option("--cron/--no-cron", default=False)
def crawl(pixiv_id, password, cron):
    words = [w for w in Word.select().order_by(Word.id)]
    crawler = PixivCrawler()
    crawler.login(pixiv_id, password)
    for word in words:
        data = {"word": word, "stored_at": date.today()}
        try:
            r = SearchResult.get(word=data["word"], stored_at=data["stored_at"])
            if not cron:
                click.echo(
                    f"【登録済】{word.text} - safe: {r.num_of_safe}件 / r18: {r.num_of_r18}件"
                )
        except SearchResult.DoesNotExist:
            for mode in ("safe", "r18"):
                crawler.search(word.text, mode)
                if mode == "safe":
                    data["safe"] = crawler.get_search_count()
                else:
                    data["r18"] = crawler.get_search_count()
                time.sleep(3)

            SearchResult.create(
                word=data["word"],
                stored_at=data["stored_at"],
                num_of_safe=data["safe"],
                num_of_r18=data["r18"],
            )
            if not cron:
                click.echo(f"{word.text} - safe: {data['safe']}件 / r18: {data['r18']}件")


if __name__ == "__main__":
    crawl()
