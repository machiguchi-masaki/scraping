import re
import time
from typing import Iterator
import requests as req
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
import sqlite3


def main():

    session = req.Session()
    response = session.get('https://gihyo.jp/dp')
    urls = scrape_list_page(response)

    for url in urls:
        time.sleep(1)
        response = session.get(url)
        ebook = scrape_detail_page(response)
        insert_sqlite(ebook)

        break


def scrape_list_page(response: req.Response) -> Iterator[str]:
    soup = bs(response.text, 'html.parser')

    for a in soup.select('#listBook > li > a[itemprop="url"]'):
        url = urljoin(response.url, a.get('href'))
        yield url


def scrape_detail_page(response: req.Response) -> dict:
    soup = bs(response.text, 'html.parser')

    ebook = {
        'url': response.url,
        # 'key':
        'title': soup.select_one('#bookTitle').text,
        'price': soup.select_one('.buy').contents[0].strip()
        # 'content'
    }

    return ebook


def insert_sqlite(ebook):

    conn = sqlite3.connect('data/ebook.db')

    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS cities')
    c.execute("""
        CREATE TABLE cities (
            url text,
            title text,
            price text
            )
        """)

    query = 'INSERT INTO cities VALUES (:url, :title, :price)'
    c.execute(query, ebook)

    conn.commit()

    c.execute('select * from cities')
    for row in c.fetchall():
        print(row)

    conn.close()


if __name__ == '__main__':
    main()
