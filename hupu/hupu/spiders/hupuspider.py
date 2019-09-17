# -*- coding: utf-8 -*-
import scrapy


class HupuspiderSpider(scrapy.Spider):
    name = 'hupuspider'
    allowed_domains = ['hupu.com']
    start_urls = ['https://bbs.hupu.com/all-gambia', 'https://soccer.hupu.com/china/']
    base_url = 'https://bbs.hupu.com'

    def parse(self, response):
        url = response.url
        if url == 'https://bbs.hupu.com/all-gambia':
            lis = response.xpath('//ul[@class="hp-threeNav-item"]/li')
            for ul in lis[1:]:
                href = ul.xpath('a/@href').extract_first('')
                type = ul.xpath('a/text()').extract_first('')
                url = self.base_url + href
                yield scrapy.Request(url=url, callback=self.parse_type, meta={'type': type})

    def parse_type(self, response):
        '''
        获取每页所有话题的url
        :param response:
        :return:
        '''
        type = response.meta['type']
        divs = response.xpath("//div[contains(@class, 'forum_row')]")
        for div in divs:
            id = 0
            url_id = div.xpath('div/strong/a/@href')[0]
            title = div.xpath('div/strong/a/text()')[0]
            content_info = []
            article_url = self.base_url + url_id

            # yield scrapy.Request(url=article_url, callback=self.parse_detail_page,
            #                      meta={'content_info': content_info, 'id': id, 'title': title, 'type': type,
            #                            'article_url': article_url})
        # next = html.xpath('//a[@class="next_link"]/@href')
        # if len(next) != 0:
        #     type = response.meta['type']
        #     next_url = self.base_url + next[0]
        #     yield scrapy.Request(url=next_url, callback=self.parse_type, meta={'type': type, })
