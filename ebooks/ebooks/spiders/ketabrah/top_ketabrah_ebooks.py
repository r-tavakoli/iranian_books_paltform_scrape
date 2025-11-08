from scrapy import Spider
from ebooks.item_loaders import KetabrahEbooksLoader
from ebooks.items import KetabrahEbooksItem
from ebooks.types import *
from urllib.parse import urlparse

class KetabrahEbook(Spider):
    """
    Scrapy Spider designed to scrape ebook and audiobook from the
    Ketabrah platform's filtered pages.
    """
    
    name = "ebook_ketabrah"
    
    # The URLs are configured to access different filtered/sorted lists.
    start_urls = [
        "https://ketabrah.com/d/ebook-bestsellers-in-month", # most popular ebooks
        "https://ketabrah.com/d/audiobook-bestsellers-in-month", # most popular audio books
        "https://ketabrah.com/d/new-releases-audiobooks?bt=audiobooks", # newest audio books
        "https://ketabrah.com/d/new-releases-ebooks?bt=books", # newest ebooks
    ]
    
    def get_category_and_book_type(self, url):
        """
        Extracts the 'book type' and 'category name' parameters from the URL
        and maps their integer values to meaningful string values using custom enums.
        """

        parsed_path = urlparse(url).path

        book_type_id = BookType.EBOOK.id if 'ebook' in parsed_path else BookType.AUDIOBOOK.id
        category_name_id = CategoryName.NEWEST.id if 'new' in parsed_path else CategoryName.MOST_POPLUAR.id

        # Map the integer index to a string using the custom BookType enum and CategoryName enum
        book_type = BookType.get_values()[book_type_id]
        category_name = CategoryName.get_values()[category_name_id]

        return book_type, category_name

    def parse(self, response):
        
        # Determine the book type and category based on the current response URL
        book_type, category_name = self.get_category_and_book_type(response.url)

        books = response.xpath("//div[starts-with(@class, 'book-list')]/div[starts-with(@class, 'book')]")


        for id, book in enumerate(books, start=1):

            loader = KetabrahEbooksLoader(item=KetabrahEbooksItem(), selector=book)
            
            # --- Load Static/Derived Fields ---
            loader.add_value("sort_id", id)
            loader.add_value("website_id", Website.KETABRAH.id)
            loader.add_value("website_name", Website.KETABRAH.text)
            loader.add_value("category_name", category_name)
            loader.add_value("book_type", book_type)
            
            # --- Load Extracted Fields (XPath) ---
            book_url = book.xpath(".//a[@class='cover']/@href").get()
            if book_url and not book_url.startswith("http"):
                book_url = response.urljoin(book_url)
            loader.add_value("url", book_url)
            loader.add_xpath("book_title", ".//h3[@itemprop='name']/text()")
            loader.add_xpath("author", ".//a[@itemprop='author']/text()")
            loader.add_xpath("rate", ".//div[@class='value']/text()")
            loader.add_xpath("votes", ".//div[@class='votes-count']/text()")
            loader.add_xpath("price", ".//span[starts-with(@class, 'main-price')]/text()")
            loader.add_xpath("selling_price", ".//span[@class='with-discount']/text()")

            yield loader.load_item()
