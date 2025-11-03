from scrapy import  Spider
from ebooks.item_loaders import EbookLoader
from rich.panel import Panel
from ebooks.items import TaaghcheEbooksItem
from ebooks.types import *

class TaaghcheMostPopularEbook(Spider):
    name = "ebook_taaghche"
    start_urls = [
        "https://taaghche.com/filter?filter-bookType=0&order=1", # most popular ebooks
        "https://taaghche.com/filter?filter-bookType=1&order=1", # most popular audio books
        
        ]

    def parse(self, response):
        print(Panel('[bold]starts here', style='green'))

        books = response.xpath("//div[starts-with(@class, 'bookCard_book_')]")

        for id, book in enumerate(books, start=1):
            loader = EbookLoader(item=TaaghcheEbooksItem(), selector=book)
            loader.add_value("sort_id", id)
            loader.add_value("website_id", Website.Taaghche.id)
            loader.add_value("website_name", Website.Taaghche.text)
            loader.add_value("category_name", CategoryName.MOST_POPLUAR.value)
            loader.add_value("book_type", BookType.EBOOK.value)
            loader.add_xpath("url", ".//a[starts-with(@class, 'bookCard_bookLink')]/@href")
            loader.add_xpath("book_title", ".//span[starts-with(@class, 'bookCard_bookTitle')]/text()")
            loader.add_xpath("author", ".//div[starts-with(@class, 'bookCard_bookAuthorName')]/text()")
            loader.add_xpath("rate", ".//span[starts-with(@class, 'bookCard_rateNumber')]/text()")
            loader.add_xpath("votes", ".//div[starts-with(@class, 'bookCard_rate')]/text()")
            loader.add_xpath("price", "..//span[starts-with(@class, 'bookCard_beforeOffPrice')]/text()")
            loader.add_xpath("selling_price", ".//span[starts-with(@class, 'bookCard_price')]/text()")

            yield loader.load_item()
