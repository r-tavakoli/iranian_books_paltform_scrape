from scrapy import Item, Field
from itemloaders.processors import MapCompose, Identity, Compose
from urllib.parse import urljoin
from datetime import datetime


class EbooksItem(Item):
    """
    Base Item class for all ebook data across different websites.
    It defines the common schema for the data being scraped.
    """

    # order of books 
    sort_id = Field() 
    website_id = Field()
    website_name = Field()
    category_name = Field()
    book_type = Field()
    url = Field()
    book_title = Field()
    author = Field()
    rate = Field()
    votes = Field()
    price = Field()         # Original price before discount (used for 'before discount' field)
    selling_price = Field() # Final selling price after discount (used for 'after discount' field)
    crawl_date = Field(default_value=datetime.now().strftime("%Y-%m-%d"))


class CsvItemExport(EbooksItem):
    """
    A placeholder Item used specifically by the CsvExportPipeline.
    """    
    pass


# --- Utility Functions for ItemLoader Processors ---
def url_join(base, url):
    """Prepends the base Taaghche URL to a relative URL fragment."""
    return urljoin(base, url)

def get_nth_item(value, n):
    """Safely retrieves the n-th item from a list of values. Returns 0 on IndexError."""
    try:
        return value[n]
    except (IndexError, TypeError):
        return 0
    
def extract_number(value):
    return ''.join(v for v in value if v.isdigit())
        



class TaaghcheEbooksItem(EbooksItem):
    """
    Specific Item definition for Taaghche data.
    It customizes the Field properties using input_processors to clean and
    convert raw string data extracted from the web page into desired types. 
    Also default_values are used specifically by the DefaultValuePipeline.
    """    
    url = Field(
        input_processor = MapCompose(lambda u: url_join("https://taaghche.com/", u))
        )       
    votes = Field(
        input_processor = Compose(Identity(), lambda v: get_nth_item(v, n=1), int),
        default_value=0
    )
    rate = Field(
        input_processor = MapCompose(lambda r: r.replace('٫', '.'), float),
        default_value=0
    )
    price = Field(
        input_processor = MapCompose(lambda p: p.replace(',', ''), int),
        default_value=0
    )
    selling_price = Field(
        input_processor = MapCompose(lambda sp: sp.replace(',', ''), int),
        default_value=0
    )


class KetabrahEbooksItem(EbooksItem):
    """
    Specific Item definition for ketabrah data.
    It customizes the Field properties using input_processors to clean and
    convert raw string data extracted from the web page into desired types. 
    Also default_values are used specifically by the DefaultValuePipeline.
    """    
    book_title = Field(
        input_processor = MapCompose(lambda i: i.lstrip('کتاب صوتی'), lambda i: i.lstrip('کتاب'), str.strip)
    )
    url = Field(
        input_processor = MapCompose(lambda u: url_join("https://ketabrah.com/", u))
        )       
    votes = Field(
        input_processor = MapCompose(extract_number, int),
        default_value=0
    )
    rate = Field(
        input_processor = MapCompose(lambda r: r.replace('٫', '.'), float),
        default_value=0
    )
    price = Field(
        input_processor = MapCompose(extract_number, int),
        default_value=0
    )
    selling_price = Field(
        input_processor = MapCompose(extract_number, int),
        default_value=0
    )