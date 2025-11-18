# omad_template/src/main.py

import requests
# import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url = 'https://books.toscrape.com'

ua = UserAgent()
headers = {'user-agent': ua.random}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
title = soup.title.text
print(title)