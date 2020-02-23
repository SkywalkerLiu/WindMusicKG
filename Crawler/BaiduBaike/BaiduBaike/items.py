# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class BaikeSingerItem(Item):
    _name = Field()
    meta = Field()
    crawled = Field()
    url = Field()

class UniqueNode(Item):
    name = Field()
    url = Field()

class ExampleLoader(ItemLoader):
    default_item_class = BaikeSingerItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
