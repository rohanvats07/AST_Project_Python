import scrapy
from pathlib import Path
from pymongo import MongoClient
import datetime

client = MongoClient("mongodb+srv://rohanvats07:ng17rv07@mongorv.wwercyk.mongodb.net/")
db = client.store_books
def inserttodb(page, title, ratting, image, price, instock):
    collection = db[page]
    doc = {
        "title": title, "ratting": ratting, "image":image, 
        "price": price, "instock": instock,
        "date": datetime.datetime.now(tz=datetime.timezone.utc),}
    inserted = collection.insert_one(doc)
    return inserted.inserted_id8


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]


    def start_requests(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"books-{page}.html"
        bookdetail = {}

        # save the content as files
        # Path(filename).write_bytes(response.body)

        # --------------------

        # self.log(f"Saved file {filename}")
        # a = response.css(".product_pod").get()
        # b = a.css("a")
        # print(b)

        # --------------------

        self.log(f"Saved file {filename}")
        cards = response.css(".product_pod")
        for card in cards:
            title = card.css("h3>a::text").get()
            # print(title)
            ratting = card.css(".star-rating").attrib["class"].split(" ")[1]
            # print(ratting)
            image = card.css(".image_container img")
            image = image.attrib["src"].replace("../../../../media","https://books.toscrape.com/media")
            # print(image.attrib["src"])
            price = card.css(".price_color::text").get()
            # print(price)
            availability = card.css(".availability")
            # print(availability)
            # print(len(availability.css(".icon-ok")))
            if len(availability.css(".icon-ok")) > 0:
                instock = True
            else:
                instock = False
            inserttodb(filename, title, ratting, image, price, instock)

