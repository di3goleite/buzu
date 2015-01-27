# -*- coding: utf-8 -*-
import scrapy

from buzu.items import BuzuItem

class SchedulesSpider(scrapy.Spider):
    name = "schedules"
    allowed_domains = ["sincolfeira.com.br"]
    start_urls = (
        'http://www.sincolfeira.com.br/horarios/cidadenova-cis-dias-uteis.html',
        #'http://www.sincolfeira.com.br/horarios/genipapo-dias-uteis.html',
    )

    # Parse Schedule Page
    def parse(self, response):
        header = response.xpath('//table//tr[1]//td/text()').extract()[1:]
        items = []
        cars = []

        for i in range(len(header)):
            # Remove Car columns
            if('Carro' in header[i] and i!=0):
                cars.append(i)

            # WTF Sincol
            if(header[i] == ' '):
                header[i] = response.xpath('//table//tr[1]//td//span/text()').extract()

        # Extract schedule
        for sel in response.xpath('//table//tr')[1:]:
            schedule = sel.xpath('td/text()').extract()[1:]

            # Remove car column from schedule
            for i in cars:
                del schedule[i]

            # Create a new BuzuItem
            item = BuzuItem()
            item['schedule'] = schedule

            items.append(item)

        return items
