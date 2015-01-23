# -*- coding: utf-8 -*-
import scrapy


class HorariosSpider(scrapy.Spider):
    name = "horarios"
    allowed_domains = ["sincolfeira.com.br"]
    start_urls = (
        'http://www.sincolfeira.com.br/meuponto.php',
    )

    def parse(self, response):
        schedule_urls = self.get_schedule_urls(response)

        for schedule_url in schedule_urls:
            yield Request(schedule_url, callback=self.parse_schedule)

    def get_schedule_urls(self, response):
        hxs = HtmlXPathSelector(response)

        for path in hxs.select("//table[@class='textos']//tr//td[3]//a//@href").extract:
            protocol = 'http://'
            domain = self.allowed_domain[0]
            yield protocol + domain + path

    def parse_schedule(self, response):
        pass
