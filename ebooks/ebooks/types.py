from enum import Enum


class BaseEnum(Enum):

    @property
    def id(self):
        return self.value[0]
    
    @property
    def text(self):
        return self.value[1]

    @classmethod
    def get_values(cls):
        return dict(map(lambda c: (c.id, c.text), cls))

class BookType(BaseEnum):
    EBOOK = (0, "ebook")
    AudioBook = (1, "audio_book")

class CategoryName(BaseEnum):
    NEWEST = (0, "newest")
    MOST_POPLUAR = (1, "most_popular")

class Website(BaseEnum):
    Taaghche = (1, "taaghche.com")
    IranKetab = (2, "iranketab.ir")   
    Fidibo = (3, "fidibo.com")