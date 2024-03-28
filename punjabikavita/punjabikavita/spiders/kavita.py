import scrapy


class KavitaSpider(scrapy.Spider):
    name = "kavita"
    allowed_domains = ["punjabi-kavita.com"]
    start_urls = ["https://punjabi-kavita.com"]

    def parse(self, response):
        pass
