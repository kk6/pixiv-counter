# -*- coding: utf-8 -*-
import time
import re

import requests
from bs4 import BeautifulSoup


class PixivCrawler:

    def __init__(self):
        self.session = requests.Session()
        self._current_response = None

    def login(self, pixiv_id, password):
        r = self.session.get(
            "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
        )
        post_key = re.search(r'name="post_key" value="(\w+)"', r.text).group(1)
        url = "https://accounts.pixiv.net/login"
        data = {
            "pixiv_id": pixiv_id,
            "password": password,
            "source": "pc",
            "lang": "ja",
            "return_to": "https://www.pixiv.net/",
            "post_key": post_key,
        }
        return self.session.post(url, data=data)

    def search(self, word, mode=None):
        url = "https://www.pixiv.net/search.php"
        params = {"s_mode": "s_tag", "word": word}
        if mode:
            params["mode"] = mode
        resp = self.session.get(url, params=params)
        self._current_response = resp
        return resp

    def get_search_count(self, html=None):
        if not html:
            html = self._current_response.text
        soup = BeautifulSoup(html, "html.parser")
        count_text = soup.find("span", class_="count-badge").text
        return int(count_text[:-1])  # 'N件' の「件」を除外して返す


def search_all(pixiv_id, password, words, mode=None):
    crawler = PixivCrawler()
    crawler.login(pixiv_id, password)
    for word in words:
        crawler.search(word, mode)
        count = crawler.get_search_count()
        print(f"{word}: {count}件")
        time.sleep(3)
