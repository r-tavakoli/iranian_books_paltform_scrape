from scrapy import Spider
from ebooks.item_loaders import TaaghcheEbooksLoader
from ebooks.items import TaaghcheEbooksItem
from ebooks.types import *
from urllib.parse import urlparse, parse_qs

class TaaghcheEbook(Spider):
    """
    Scrapy Spider designed to scrape ebook and audiobook from the
    Taaghche platform's filtered pages.
    """
    
    name = "ebook_taaghche"
    
    # The URLs are configured to access different filtered/sorted lists.
    start_urls = [
        "https://taaghche.com/filter?filter-bookType=0&order=1", # most popular ebooks
        "https://taaghche.com/filter?filter-bookType=1&order=1", # most popular audio books
        "https://taaghche.com/filter?filter-bookType=0&order=0", # newest ebooks
        "https://taaghche.com/filter?filter-bookType=1&order=0", # newest audio books
    ]
    
    def get_category_and_book_type(self, url):
        """
        Extracts the 'book type' and 'category name' parameters from the URL
        and maps their integer values to meaningful string values using custom enums.
        """
        # Parse the URL to extract the query parameters
        parsed_params = parse_qs(urlparse(url).query)
        book_type_id = int(parsed_params['filter-bookType'][0])
        category_name_id = int(parsed_params['order'][0])

        # Map the integer index to a string using the custom BookType enum and CategoryName enum
        book_type = BookType.get_values()[book_type_id]
        category_name = CategoryName.get_values()[category_name_id]

        return book_type, category_name

    def parse(self, response):
        
        # Determine the book type and category based on the current response URL
        book_type, category_name = self.get_category_and_book_type(response.url)

        books = response.xpath("//div[starts-with(@class, 'bookCard_book_')]")

        for id, book in enumerate(books, start=1):

            loader = TaaghcheEbooksLoader(item=TaaghcheEbooksItem(), selector=book)
            
            # --- Load Static/Derived Fields ---
            loader.add_value("sort_id", id)
            loader.add_value("website_id", Website.TAAGHCHE.id)
            loader.add_value("website_name", Website.TAAGHCHE.text)
            loader.add_value("category_name", category_name)
            loader.add_value("book_type", book_type)
            
            # --- Load Extracted Fields (XPath) ---
            book_url = book.xpath(".//a[starts-with(@class, 'bookCard_bookLink')]/@href").get()
            if book_url and not book_url.startswith("http"):
                book_url = response.urljoin(book_url)
            loader.add_value("url", book_url)
            loader.add_xpath("book_title", ".//span[starts-with(@class, 'bookCard_bookTitle')]/text()")
            loader.add_xpath("author", ".//div[starts-with(@class, 'bookCard_bookAuthorName')]/text()")
            loader.add_xpath("rate", ".//span[starts-with(@class, 'bookCard_rateNumber')]/text()")
            loader.add_xpath("votes", ".//div[starts-with(@class, 'bookCard_rate')]/text()")
            loader.add_xpath("price", ".//span[starts-with(@class, 'bookCard_beforeOffPrice')]/text()")
            loader.add_xpath("selling_price", ".//span[starts-with(@class, 'bookCard_price')]/text()")

            yield loader.load_item()
