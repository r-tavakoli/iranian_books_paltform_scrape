from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst

class EbookLoader(ItemLoader):
    default_output_processor = TakeFirst()