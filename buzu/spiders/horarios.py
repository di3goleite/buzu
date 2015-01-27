# -*- coding: utf-8 -*-
import scrapy

from buzu.items import BuzuItem

class HorariosSpider(scrapy.Spider):
    name = "horarios"
    allowed_domains = ["sincolfeira.com.br"]
    start_urls = (
        'http://www.sincolfeira.com.br/horarios/cidadenova-cis-dias-uteis.html',
        #'http://www.sincolfeira.com.br/horarios/genipapo-dias-uteis.html',
    )

    def parse(self, response):
        header = response.xpath('//table//tr[1]//td/text()').extract()[1:]

        items = []
        cars = []

        for i in range(len(header)):
            if('Carro' in header[i] and i!=0):
                cars.append(i)

            if(header[i] == ' '):
                header[i] = response.xpath('//table//tr[1]//td//span/text()').extract()

        for sel in response.xpath('//table//tr')[1:]:
            schedule = sel.xpath('td/text()').extract()[1:]

            for i in cars:
                del schedule[i]

            item = BuzuItem()
            item['schedule'] = schedule

            items.append(item)

        return items
