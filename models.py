from mongoengine import *


uri = "mongodb+srv://goitlearn:goit_web_db_mongodb@cluster0.sgtae2n.mongodb.net/hw_09?retryWrites=true&w=majority"

connect(host=uri, ssl=True)


class Author(Document):
    fullname = StringField(max_length=50)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = (
        StringField()
    )


class Quote(Document):
    tags = ListField(max_length=50)
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {"allow_inheritance": True}
