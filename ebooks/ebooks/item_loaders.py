from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst

class EbookLoader(ItemLoader):
    default_output_processor = TakeFirst()


class TaaghcheEbooksLoader(EbookLoader):
    pass

class KetabrahEbooksLoader(EbookLoader):
    pass

class FidiboEbooksLoader(EbookLoader):
    pass