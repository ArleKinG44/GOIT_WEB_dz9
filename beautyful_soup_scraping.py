import re
import json

import requests
from bs4 import BeautifulSoup


def get_authors() -> list:

    base_url = "https://quotes.toscrape.com/page/"
    list_authors = []
    for i in range(1, 11):
        response = requests.get(base_url + str(i))
        soup = BeautifulSoup(response.text, "html.parser")
        content_authors = soup.select("small[class=author]")
        for elem in content_authors:
            autor_name = re.search(r">.+</", str(elem)).group()[1:-2]
            list_authors.append(autor_name)
    return list_authors


def get_quotes() -> list:

    base_url = "https://quotes.toscrape.com/page/"
    list_quotes = []
    for i in range(1, 11):
        response = requests.get(base_url + str(i))
        soup = BeautifulSoup(response.text, "html.parser")
        content_quotes = soup.select("span[class=text]")
        for elem in content_quotes:
            quote = re.search(r">.+</", str(elem)).group()[2:-3]
            list_quotes.append(quote)
    return list_quotes


def get_tags() -> list:

    base_url = "https://quotes.toscrape.com/page/"
    list_tags = []
    for i in range(1, 11):
        response = requests.get(base_url + str(i))
        soup = BeautifulSoup(response.text, "html.parser")
        content_tags = soup.select("div[class=tags]")
        for elem in content_tags:
            tag = re.findall(r">.+</", str(elem))
            tag_clean = []
            for el in tag:
                tag_clean.append(el[1:-2])
            list_tags.append(tag_clean)
    return list_tags


def create_quotes_json(
    list_of_names: get_authors(), list_of_tags: get_tags(), list_of_quotes: get_quotes()
) -> None:

    result = []
    for i in range(len(list_of_names)):
        dct = {}
        dct["tags"] = list_of_tags[i]
        dct["author"] = list_of_names[i]
        dct["quote"] = list_of_quotes[i]
        result.append(dct)
    with open("quotes.json", "w") as a:
        json.dump(result, a)


def list_urls_about(list_of_names: get_authors()) -> list:

    base_url = "http://quotes.toscrape.com/author/"
    lst_authors_names = []
    lst_authors_urls = []
    for i in list_of_names:
        if i[-1] == ".":
            lst_authors_names.append(
                i[:-1].replace(" ", "-").replace("--", "-").replace("é", "e")
            )
        else:
            lst_authors_names.append(
                i.replace(" ", "-")
                .replace(".", "-")
                .replace("--", "-")
                .replace("é", "e")
                .replace("'", "")
            )
    for b in lst_authors_names:
        lst_authors_urls.append(base_url + str(b))
    return list(set(lst_authors_urls))


def create_authors_json(
    list_of_names: get_authors(), list_urls: list_urls_about(get_authors())
) -> None:

    list_dates_authors = []
    list_copy = list_of_names.copy()
    for address in list_urls:
        dct = {}
        dct["fullname"] = list_copy[0]
        list_copy.pop(0)

        response = requests.get(address)
        soup = BeautifulSoup(response.text, "html.parser")

        content_born_date = soup.select("span[class=author-born-date]")
        try:
            dct["born_date"] = re.search(r">.+</", str(content_born_date[0])).group()[
                1:-2
            ]
        except AttributeError:
            print(f"Error in parsing born_date on: {address}")

        content_born_location = soup.select("span[class=author-born-location]")
        try:
            dct["born_location"] = re.search(
                r">.+</", str(content_born_location[0])
            ).group()[1:-2]
        except AttributeError:
            print(f"Error in parsing born_location on: {address}")

        content_description = soup.select("div[class=author-description]")
        try:
            dct["description"] = re.search(
                r"   .+   ", content_description[0].text
            ).group()[8:-4]
        except AttributeError:
            print(f"Error in parsing description on: {address}")

        list_dates_authors.append(dct)
    with open("authors.json", "w") as a:
        json.dump(list_dates_authors, a)


if __name__ == "__main__":
    list_of_names = get_authors()
    list_of_tags = get_tags()
    list_of_quotes = get_quotes()
    create_quotes_json(list_of_names, list_of_tags, list_of_quotes)
    list_urls = list_urls_about(list_of_names)
    create_authors_json(list_of_names, list_urls)

    print("Done")
