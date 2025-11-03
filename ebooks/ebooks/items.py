from scrapy import Item, Field
from itemloaders.processors import MapCompose, Identity, Compose
from urllib.parse import urljoin

class EbooksItem(Item):
    sort_id = Field() # order of books 
    website_id = Field()
    website_name = Field()
    category_name = Field()
    book_type = Field()
    url = Field()
    book_title = Field()
    author = Field()
    rate = Field()
    votes = Field()
    price = Field() # before discount
    selling_price = Field() # after discount
    crawl_date = Field()


# taaghche Item
def url_join(url):
    return urljoin("https://taaghche.com", url)

def get_nth_item(value, n):
    try:
        return value[n]
    except IndexError:
        return 0


class TaaghcheEbooksItem(EbooksItem):
    url = Field(
        input_processor = MapCompose(url_join)
        )       
    votes = Field(
        output_processor = Compose(Identity(), lambda v: get_nth_item(v, n=1), int)
    )
    rate = Field(
        input_processor = MapCompose(lambda r: r.replace('٫', '.'), float)
    )
    price = Field(
        input_processor = MapCompose(lambda p: p.replace(',', ''), int)
    )
    selling_price = Field(
        input_processor = MapCompose(lambda sp: sp.replace(',', ''), int)
    )