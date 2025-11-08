from scrapy import Spider, Request
from scrapy.http import HtmlResponse
from scrapy_playwright.page import PageMethod
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
        "https://fidibo.com/contents/list?sort=POPULAR&types=[2]", # most popular audio books
        "https://fidibo.com/contents/list?sort=RECENT&types=[2]", # newest audio books
        "https://fidibo.com/contents/list?sort=RECENT&types=[1]", # newest ebooks
    ]

    
    def get_category_and_book_type(self, url):
        """
        Extracts the 'book type' and 'category name' parameters from the URL
        and maps their integer values to meaningful string values using custom enums.
        """

        parsed_params = parse_qs(urlparse(url).query)
        type_extracted = ''.join(i for i in parsed_params['types'][0] if i.isdigit())
        sort_extracted = parsed_params['sort'][0]

        book_type_id = BookType.AUDIOBOOK.id if int(type_extracted) == 2 else BookType.EBOOK.id
        category_name_id = CategoryName.NEWEST.id if 'RECENT' in sort_extracted else CategoryName.MOST_POPLUAR.id

        # Map the integer index to a string using the custom BookType enum and CategoryName enum
        book_type = BookType.get_values()[book_type_id]
        category_name = CategoryName.get_values()[category_name_id]

        return book_type, category_name


    def start_requests(self):
        for url in self.urls_to_scrape:
            yield Request(
                url,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        # Wait for actual content instead of network idle
                        PageMethod("wait_for_selector", "img[src*='cdn.fidibo.com']", timeout=20000),
                    ],
                    playwright_context_kwargs={
                        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "viewport": {"width": 1920, "height": 1080},
                    },
                    # errback=self.errback,
                ),
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        # Wait a bit more for dynamic content
        await page.wait_for_timeout(5000)
        
        # Take screenshot to verify what we're seeing
        # try:
        #     await page.screenshot(path="fidibo_rendered.png", full_page=True)
        #     self.logger.info("Screenshot saved as fidibo_rendered.png")
        # except Exception as e:
        #     self.logger.warning(f"Screenshot failed: {e}")
        
        # Get the fully rendered HTML
        content = await page.content()
        
        # Save HTML for manual inspection
        # with open("fidibo_full_page.html", "w", encoding="utf-8") as f:
        #     f.write(content)

        # Determine the book type and category based on the current response URL
        self.book_type, self.category_name = self.get_category_and_book_type(response.url)       
        
        self.logger.info("Full page HTML saved")
        
        # Extract visible data
        async for book_item in self.extract_visible_books(content, response.url):
            yield book_item
        
        await page.close()
    

    async def extract_visible_books(self, html_content, response_url):
        """Extract books from the visible page content"""
        response = HtmlResponse(url=response_url, body=html_content, encoding='utf-8')

        # Look for book card cantainers
        books = response.xpath("//a[contains(@class, 'content-card-container-item')]")

        # Look for book info
        for id, book in enumerate(books, start=1):


            loader = FidiboEbooksLoader(item=FidiboEbooksItem(), selector=book)
            
            # --- Load Static/Derived Fields ---
            loader.add_value("sort_id", id)
            loader.add_value("website_id", Website.FIDIBO.id)
            loader.add_value("website_name", Website.FIDIBO.text)
            loader.add_value("category_name", self.category_name)
            loader.add_value("book_type", self.book_type)

            # --- Load Extracted Fields (XPath) ---
            
            book_url = book.xpath("@href").get()
            if book_url and not book_url.startswith("http"):
                book_url = response.urljoin(book_url)
            loader.add_value("url", book_url)
            loader.add_xpath("book_title", ".//div[contains(@class, 'content-title')]/text()")
            loader.add_xpath("author", ".//div[contains(@class, 'content-subtitle')]/text()")
            loader.add_xpath("rate", ".//div[contains(@class, 'content-rate-score')]/text()")
            loader.add_xpath("votes", ".//div[contains(@class, 'content-rate-responses')]/text()")
            loader.add_xpath("price",  ".//div[contains(@class, 'content-price-discount')]/text()")
            loader.add_xpath("selling_price", ".//div[contains(@class, 'content-price-number')]/text()")


            yield loader.load_item()