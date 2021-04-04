from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta, timezone
import pandas as pd
import csv

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
d = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
url = 'https://www.mercari.com/jp/search/?sort_order=created_desc&keyword=%E3%82%AC%E3%83%A9%E3%83%AB%E3%83%95%E3%82%A1%E3%82%A4%E3%83%A4%E3%83%BCV&category_root=1328&category_child=82&category_grand_child%5B1289%5D=1&brand_name=&brand_id=&size_group=&price_min=5000&price_max=&status_trading_sold_out=1'
d.get(url)

item = d.find_elements_by_css_selector(".items-box")

soup = BeautifulSoup(d.page_source, 'html.parser')
items = soup.select('.items-box')

columns = ["Name", "Price", "Link", "Date"]
# 配列名を指定する
df = pd.DataFrame(columns=columns)


for item in items:

    # 商品名
    name = item.select_one('.items-box-name').string

    # 値段
    price = item.select_one('.items-box-price').string
    price = price.replace("¥", "")
    price = price.replace(",", "")

    # リンク
    link = 'https://www.mercari.com' + item.a['href']

    # 画像
    img = item.img['data-src']

    # 出品日
    img_re = re.search(r'jpg(.*)', img)
    dt_utc = int(img_re.group(1).replace('?', ''))
    dt_utc = datetime.utcfromtimestamp(dt_utc)
    dt = dt_utc.date()

    # 追記
    se = pd.Series([name, price, link, dt], columns)
    df = df.append(se, columns)


df.to_csv('data/fire.csv', encoding='utf-8-sig')

d.quit()
