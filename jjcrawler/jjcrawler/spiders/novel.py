import scrapy


class NovelSpider(scrapy.Spider):
    name = "novel"
    allowed_domains = ["www.jjwxc.net"]
    start_urls = ["https://www.jjwxc.net"]

    def parse(self, response):
        pass
