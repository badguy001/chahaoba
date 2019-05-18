# -*- coding: UTF-8 -*-

import scrapy
from chahaoba.items import ChahaobaItem

class Daemon(scrapy.Spider):
    name = "chahaoba"
    start_urls = [
        "https://www.chahaoba.com/%E6%89%8B%E6%9C%BA%E5%BD%92%E5%B1%9E"
    ]

    def parse(self, response):
        assert isinstance(response, scrapy.http.response.Response)
        sel = response.xpath('//div[@id="mw-content-text"]/ul/li/a[not (@class="new")]/..')
        sjhd_list = []
        for li in sel:
            sjhd = li.xpath('a[1]/text()').extract()[0]
            sjhd = sjhd[0:3]
            if sjhd in sjhd_list:
                continue
            sjhd_list.append(sjhd)
            url = response.urljoin('/'+sjhd)
            yys = li.xpath('a[1]/following-sibling::a[1]/text()').re(u'(联通|电信|移动)$')
            if len(yys) == 0:
                yys = li.xpath('a[1]/following-sibling::text()').re(u'(联通|电信|移动)$')
            if len(yys) == 0:
                yys = ""
            else:
                yys = yys[0]
            yield scrapy.Request(url=url, callback=self.parse_threed, meta={'sjhd': sjhd, 'yys': yys})


    def parse_threed(self, response):
        assert isinstance(response, scrapy.http.response.Response)
        sjhd = response.meta['sjhd']
        yys = response.meta['yys']
        sel = response.xpath('//div[@id="mw-content-text"]/p/a[not (@class="new") and contains(text(),"'+sjhd+'")]/..')
        for every_sf in sel:
            sf = every_sf.xpath('preceding-sibling::h3[1]//a/text()').extract()[0].replace(sjhd,'')
            for every_ds in every_sf.xpath('a[not (@class="new") and contains(text(),"'+sjhd+'")]'):
                ds = every_ds.xpath('text()').extract()[0].replace(sjhd,'')
                url = response.urljoin(every_ds.xpath('@href').extract()[0])
                yield scrapy.Request(url=url, callback=self.parse_seven, meta={'sjhd': sjhd, 'yys': yys,'ds':ds,'sf':sf})


    def parse_seven(self, response):
        assert isinstance(response, scrapy.http.response.Response)
        sel = response.xpath('//div[@id="myarticle"]//li')
        for every_hd in sel:
            sjhm = every_hd.xpath('a/text()').extract()[0]
            item = ChahaobaItem()
            item['sjhm'] = sjhm
            if response.meta['yys'] == u'移动':
                item['yys'] = 'Y'
            elif response.meta['yys'] == u'联通':
                item['yys'] = 'L'
            elif response.meta['yys'] == u'电信':
                item['yys'] = 'D'
            else:
                item['yys'] = response.meta['yys']
            item['sf'] = response.meta['sf']
            item['ds'] = response.meta['ds']
            yield  item