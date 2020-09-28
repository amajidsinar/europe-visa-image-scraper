import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://www.consilium.europa.eu/prado/en/prado-documents/DEU/B/O/docs-per-type.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        with open('BO.html', 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)