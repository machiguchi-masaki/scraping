import csv
from typing import List

import requests
import lxml.html


def main():
    """
    メイン処理
    """
    url = 'https://www.pokemon-card.com/card-search/'
    html = fetch(url)
    books = scrape(html, url)
    save('work/pokemon.csv', books)


def fetch(url: str) -> str:
    r = requests.get(url)
    return r.text


def scrape(html: str, base_url: str) -> List[dict]:
    books = []
    html = lxml.html.fromstring(html)
    html.make_links_absolute(base_url)

    for a in html.cssselect('#listBook > li > a[itemprop="url"]'):
        url = a.get('href')
        p = a.cssselect('p[itemprop="name"]')[0]
        title = p.text_content()

        books.append({'url': url, 'title': title})

    return books


def save(file_path: str, books: List[dict]):

    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, ['url', 'title'])
        writer.writeheader()
        writer.writerows(books)


if __name__ == '__main__':
    main()
