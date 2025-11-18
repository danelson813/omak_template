# omad_template/src/main.py
import duckdb
import requests
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url = 'https://books.toscrape.com'

def get_soup(url: str) -> BeautifulSoup: 
    ua = UserAgent()
    headers = {'user-agent': ua.random}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_books(soup: BeautifulSoup) -> list:
    books = soup.find_all('article')
    return books


def parse_pages(books_: list) -> list:
    results =[]
    for book in books_:
        title = book.find('img')['alt']
        price = book.find('p', class_='price_color').text[1:]
        print(title, price)
        result = {'title': title, 'price': price}
        results.append(result)
    return results



if __name__ == '__main__':
    soup = get_soup(url)
    books = get_books(soup)
    results = parse_pages(books)
    df = pd.DataFrame(results)
    df.to_csv("src/data/results.csv", index=False)
    conn = duckdb.connect('src/data/results.db')
    q = """
        CREATE OR REPLACE TABLE book_info (
            title VARCHAR,
            price DOUBLE)
    """
    conn.execute(q)
    conn.sql("""
        INSERT INTO book_info (title, price)
             SELECT * FROM df;
        """)
    
    # text the db
    df1 = conn.sql('SELECT * FROM book_info;').df()
    print(df1.info())
    conn.close()
