import scrapy

class MovieSpider(scrapy.Spider):
    name = "movie"

    def start_requests(self):
        urls = [
            'https://movie.douban.com/subject/11526817/'
        ]
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        yield {
            'INFOMa': response.xpath('//div[@id = "info"]/span[@class = "pl"]/text()')
        }
