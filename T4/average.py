import scrapy
from pymongo import MongoClient
import datetime
import numpy as np

client = MongoClient("mongodb+srv://rohanvats07:ng17rv07@mongorv.wwercyk.mongodb.net/")
db = client.store_books


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/category/books/travel_2/index.html"]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"books-{page}.html"
        prices = []

        self.log(f"Saved file {filename}")
        cards = response.css(".product_pod")
        for card in cards:
            title = card.css("h3 > a::text").get()
            price = card.css(".price_color::text").get()
            if title and price:
                prices.append(float(price.replace('£', '')))

        # Insert data into MongoDB (you can uncomment this if you want to store the data)
        # for card in cards:
        #     title = card.css("h3 > a::text").get()
        #     ratting = card.css(".star-rating").attrib["class"].split(" ")[1]
        #     image = card.css(".image_container img").attrib["src"].replace("../../../../media", "https://books.toscrape.com/media")
        #     availability = card.css(".availability")
        #     instock = len(availability.css(".icon-ok")) > 0
        #     inserttodb(filename, title, ratting, image, price, instock)

        yield {"average_price": np.mean(prices)}

# Run the spider
if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(BooksSpider)
    process.start()
