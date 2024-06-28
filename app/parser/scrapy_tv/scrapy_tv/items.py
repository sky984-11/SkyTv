# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyTvItem(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    description = scrapy.Field()
    total_episodes = scrapy.Field()
    rating = scrapy.Field()
    type = scrapy.Field()
    episode = scrapy.Field()
    link = scrapy.Field()
    source = scrapy.Field()
