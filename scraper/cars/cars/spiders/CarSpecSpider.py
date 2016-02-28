import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json

class CarSpecSpider(CrawlSpider):
    name = 'CarSpec'
    allowed_domains = ['www.leftlanenews.com']
    master_dictionary = {}
    start_urls = ['http://www.thecarconnection.com/new-cars/',
     "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
     "http://www.thecarconnection.com/specifications/maserati_ghibli_2016_4dr-sdn",
     "http://www.leftlanenews.com/new-car-buying/acura/rlx/specifications/"]

    rules = (
        # Extract links matching 'specifications' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('specifications/', )), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('new-car-buying', ))),
    )

    def dump_dict(self):
        with open('data.json', 'w') as fp:
            json.dump(self.master_dictionary, fp)

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        title = response.xpath("//title/text()").extract()[0]
        dictionary = {}
        dictionary['title'] = title
        filename = title.replace(" ", "") + '.txt'
        with open(filename, 'wb') as f:
            specs = response.xpath('//ul[@class="specs"]/li/ul/li/span')
            for spec in specs:
                second_half = spec.extract().split("id=")[1]
                splits = second_half.replace('"', "").split('>')
                key = splits[0]
                value = splits[1].split("<")[0]
                dictionary[key] = value
            f.write(str(dictionary))
        # This is a unique id: '#specifications'
        self.master_dictionary[title] = dictionary
        self.dump_dict()
        return dictionary