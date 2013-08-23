# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class MapperItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class H1Item(Item):
    name = Field()

class DgukSurveyItem(Item):
    url = Field()
    title = Field()
    local_links = Field()
    offsite_links = Field()
    body_class = Field()


class DmozItem(Item):
    title = Field()
    link = Field()
    desc = Field()
