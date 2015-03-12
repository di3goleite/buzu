# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from buzu.items import BuzuItem

class SchedulesSpider(scrapy.Spider):
    name = "schedules"
    allowed_domains = ["sincolfeira.com.br"]
    start_urls = (
        'http://www.sincolfeira.com.br/meuponto.php',
    )

    # Main parse funcion
    def parse(self, response):
        schedules_urls = self.get_schedules_urls(response)

        # Parse schedule_url page and return a json
        for schedule_url in schedules_urls:
            yield Request(schedule_url, callback=self.parse_schedule)

    # Get all URLs from MeuPonto page
    def get_schedules_urls(self, response):
        for schedule_url in response.xpath('//table[@class="textos"]//tr//td//a[@class="textos_p"]//@href').extract():
            protocol = 'http://'
            domain = self.allowed_domains[0]+'/'

            # Add horarios string on url, if don't have this
            if schedule_url[:9] != 'horarios/':
                schedule_url = 'horarios/'+schedule_url

            yield protocol + domain + schedule_url

    # Parse Schedule Page
    def parse_schedule(self, response):
        header = response.xpath('//table//tr[1]//td[@class="style1"]/text()').extract()[1:]
        schedule = []
        cars = []

        for i in range(len(header)):
            # Remove Car columns
            if('Carro' in header[i] and i!=0):
                cars.append(i)

            # WTF Sincol
            if(header[i] == ' '):
                header[i] = response.xpath('//table//tr[1]//td//span/text()').extract()

        # Create a new BuzuItem
        item = BuzuItem()
        item['route'] = response.xpath('//h2[@class="textos_m"]/text()').extract()
        item['source'] = response.url[35:-5]
        item['terminals'] = header

        # Extract schedule
        for sel in response.xpath('//table//tr')[1:]:
            time = sel.xpath('td/text()').extract()[1:]

            # Remove car column from schedule
            for i in cars:
                del time[i]

            # Add stoptime on schedule array
            schedule.append(time)

        # Add schedule of buzu
        item['schedule'] = schedule

        return item
