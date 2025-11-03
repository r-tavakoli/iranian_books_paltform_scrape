from enum import Enum

class BookType(Enum):
    EBOOK = (0, "ebook")
    AudioBook = (1, "audio_book")

    @property
    def id(self):
        return self.value[0]
    
    @property
    def text(self):
        return self.value[1]


class CategoryName(Enum):
    MOST_POPLUAR = (1, "most_popular")
    NEWEST = (2, "newest")

    @property
    def id(self):
        return self.value[0]
    
    @property
    def text(self):
        return self.value[1]


class Website(Enum):
    Taaghche = (1, "taaghche.com")
    IranKetab = (2, "iranketab.ir")   
    Fidibo = (3, "fidibo.com")

    @property
    def id(self):
        return self.value[0]
    
    @property
    def text(self):
        return self.value[1]