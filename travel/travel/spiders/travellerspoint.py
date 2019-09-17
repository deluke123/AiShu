# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
from ..util import clean_time
import re


from ..items import TravelItem
import time


class TravellerspointSpider(scrapy.Spider):
    name = 'travellerspoint'
    allowed_domains = ['www.travellerspoint.com']
    start_urls = ['https://www.travellerspoint.com/forum.cfm']
    base_url = 'https://www.travellerspoint.com'
    n = 0

    def parse(self, response):
        '''
        获取每页五十个url
        :param response:
        :return:
        '''
        html = etree.HTML(response.text)
        divs = html.xpath('//div[@class="rb"]//li')
        for div in divs:
            url_id = div.xpath('a/@href')[0]
            type = div.xpath('a/text()')[0]
            article_url = self.base_url + url_id
            print(article_url, type)
            yield scrapy.Request(url=article_url, callback=self.parse_type, meta={'type': type})

    def parse_type(self, response):
        '''
        获取每页五十个url
        :param response:
        :return:
        '''
        type = response.meta['type']
        html = etree.HTML(response.text)
        divs = html.xpath("//div[contains(@class, 'forum_row')]")
        for div in divs:
            id = 0
            url_id = div.xpath('div/strong/a/@href')[0]
            title = div.xpath('div/strong/a/text()')[0]
            content_info = []
            article_url = self.base_url + url_id

            yield scrapy.Request(url=article_url, callback=self.parse_detail_page, meta={'content_info': content_info, 'id': id, 'title': title, 'type': type, 'article_url': article_url})
        next = html.xpath('//a[@class="next_link"]/@href')
        if len(next) != 0:
            type = response.meta['type']
            next_url = self.base_url + next[0]
            yield scrapy.Request(url=next_url, callback=self.parse_type, meta={'type': type, })

    def parse_detail_page(self, response):
        '''
        访问解析每一个标题下面的回复：以及下一页回复
        :param response:
        :return:
        '''
        html = etree.HTML(response.text)
        content_info = response.meta['content_info']
        divs = html.xpath('//div[@class="entry"]')
        title = response.meta['title']
        type = response.meta['type']
        article_url = response.meta['article_url']
        for div in divs:
            text = div.xpath('p/text()')
            content = ''
            for t in text:
                if not re.findall(r'.*Edit: Edited on (.*?) by.*', t):
                    content += t
            # print(content)
            reply_id = 0
            user_name = div.xpath('div//a[@class="member_link"]/text()')[0]

            date_time = div.xpath('div/span[@class="post_time"]/text()')[1].strip()
            publish_time = clean_time.cleantime(date_time)
            response.meta['id'] += 1
            id = response.meta['id']
            dic1 = {'content': content, 'reply_id': reply_id, 'user_name': user_name, 'publish_time': publish_time,
                    'id': id}
            content_info.append(dic1)
        next = html.xpath('//a[@class="next_link"]/@href')
        if len(next) != 0:
            next_url = self.base_url + next[0]

            yield scrapy.Request(url=next_url, callback=self.parse_detail_page,
                                 meta={'content_info': content_info, 'id': response.meta['id'], 'title': title,
                                       'article_url': article_url, 'type': type})
        # print(content_info, type, title)
        spider_type = '论坛'
        scrawl_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        source = 'travellerspoint'
        item = TravelItem()
        item['title'] = title
        item['content_info'] = content_info
        item['article_url'] = article_url
        item['spider_type'] = spider_type
        item['scrawl_time'] = scrawl_time
        item['source'] = source
        item['type'] = type
        yield item
