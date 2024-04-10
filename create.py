from models import Author, Quote
import json


if __name__ == "__main__":
    with open("authors.json", "r", encoding="utf-8") as fh:
        data_authors = json.load(fh)
    with open("quotes.json", "r", encoding="utf-8") as fh:
        data_quotes = json.load(fh)

    for i in range(0, len(data_authors)):
        Author(
            fullname=data_authors[i]["fullname"],
            born_date=data_authors[i]["born_date"],
            born_location=data_authors[i]["born_location"],
            description=data_authors[i]["description"],
        ).save()
    for i in range(0, len(data_quotes)):
        quote = Quote(
            tags=data_quotes[i]["tags"],
            author=data_quotes[i]["author"],
            quote=data_quotes[i]["quote"],
        ).save()
