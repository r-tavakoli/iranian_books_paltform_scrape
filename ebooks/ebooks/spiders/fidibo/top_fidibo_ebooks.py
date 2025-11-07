from scrapy import Spider
from ebooks.item_loaders import FidiboEbooksLoader
from ebooks.items import FidiboEbooksItem
from ebooks.types import *
from urllib.parse import urlparse, parse_qs

class FidiboEbook(Spider):
    """
    Scrapy Spider designed to scrape ebook and audiobook from the
    Fidibo platform's filtered pages.
    """
    
    name = "ebook_fidibo"
    
    # The URLs are configured to access different filtered/sorted lists.
    urls_to_scrape = [
        "https://fidibo.com/contents/list?sort=POPULAR&types=[1]", # most popular ebooks
        # "https://fidibo.com/contents/list?sort=POPULAR&types=[2]", # most popular audio books
        # "https://fidibo.com/contents/list?sort=RECENT&types=[2]", # newest audio books
        # "https://fidibo.com/contents/list?sort=RECENT&types=[1]", # newest ebooks
    ]
    
    def get_category_and_book_type(self, url):
        """
        Extracts the 'book type' and 'category name' parameters from the URL
        and maps their integer values to meaningful string values using custom enums.
        """

        parsed_params = parse_qs(urlparse(url).query)
        type_extracted = ''.join(i for i in parsed_params['types'][0] if i.isdigit())
        sort_extracted = parsed_params['sort'][0]

        book_type_id = BookType.EBOOK.id if int(type_extracted) == 2 else BookType.AUDIOBOOK.id
        category_name_id = CategoryName.NEWEST.id if 'RECENT' in sort_extracted else CategoryName.MOST_POPLUAR.id

        # Map the integer index to a string using the custom BookType enum and CategoryName enum
        book_type = BookType.get_values()[book_type_id]
        category_name = CategoryName.get_values()[category_name_id]

        return book_type, category_name
    
    # def start_requests(self):
    #     for url in self.urls_to_scrape:
    #         yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        
        try:
            driver = response.meta['driver']
            print('Selenium WebDriver is successfully accessible!', driver)
        except KeyError as e:
            print('oh no......................................... (Should not happen)')    
            print(e)   
        # Determine the book type and category based on the current response URL
        book_type, category_name = self.get_category_and_book_type(response.url)



        # books = response.xpath("//div[starts-with(@class, 'content-card-container')]/a[contains(@class, 'content-card-container-item')]")

        # print(books)

        # for id, book in enumerate(books, start=1):

            # loader = FidiboEbooksLoader(item=FidiboEbooksItem(), selector=book)

            # # --- Load Static/Derived Fields ---
            # loader.add_value("sort_id", id)
            # loader.add_value("website_id", Website.KETABRAH.id)
            # loader.add_value("website_name", Website.KETABRAH.text)
            # loader.add_value("category_name", category_name)
            # loader.add_value("book_type", book_type)

            # # --- Load Extracted Fields (XPath) ---
            # loader.add_xpath("url", ".//a[@class='cover']/@href")
            # loader.add_xpath("book_title", ".//h3[@itemprop='name']/text()")
            # loader.add_xpath("author", ".//a[@itemprop='author']/text()")
            # loader.add_xpath("rate", ".//div[@class='value']/text()")
            # loader.add_xpath("votes", ".//div[@class='votes-count']/text()")
            # loader.add_xpath("price", ".//span[starts-with(@class, 'main-price')]/text()")
            # loader.add_xpath("selling_price", ".//span[@class='with-discount']/text()")

            # yield loader.load_item()