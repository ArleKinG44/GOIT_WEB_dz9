import requests
from bs4 import BeautifulSoup
from models import Author, Quote
import json

def scrape_quotes(url):
    all_quotes = []
    all_authors = set()
    page = 1

    while True:
        response = requests.get(url.format(page))
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all(class_='quote')

        if not quotes:
            break

        for quote in quotes:
            text = quote.find(class_='text').get_text()
            author_name = quote.find(class_='author').get_text()
            tags = [tag.get_text() for tag in quote.find_all(class_='tag')]
            all_quotes.append({'quote': text, 'author': author_name, 'tags': tags})
            all_authors.add(author_name)

        page += 1

    return all_quotes, all_authors

def save_quotes_to_json(quotes, authors, quotes_file, authors_file):
    with open(quotes_file, 'w', encoding='utf-8') as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)

    author_list = [{'fullname': author, 'born_date': '', 'born_location': '', 'description': ''} for author in authors]
    with open(authors_file, 'w', encoding='utf-8') as f:
        json.dump(author_list, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    quotes_data, authors_data = scrape_quotes('http://quotes.toscrape.com/page/{}')
    save_quotes_to_json(quotes_data, authors_data, 'quotes.json', 'authors.json')
