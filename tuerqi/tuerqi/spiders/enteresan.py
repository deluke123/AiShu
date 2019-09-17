# -*- coding: utf-8 -*-
import scrapy
from lxml import etree
import time
from ..items import TuerqiItem
import re


class EnteresanSpider(scrapy.Spider):
    name = 'enteresan'
    allowed_domains = ['www.enteresan.com']
    start_urls = ['https://www.enteresan.com']
    base_url = 'https://www.enteresan.com'

    # f = open('url.txt', 'a+', encoding='utf-8')

    def parse(self, response):
        '''
        获取每页五十个url
        :param response:
        :return:
        '''
        # html = etree.HTML(response.text)
        lis = response.xpath('//ul[@class="topMenuNoIcons"]/li')
        for li in lis[:3]:
            url_id = li.xpath('a/@href').extract_first()
            type = li.xpath('a/text()').extract_first()
            article_url = self.base_url + url_id
            print(article_url, type)
            yield scrapy.Request(url=article_url, callback=self.parse_type, meta={'type': type})

    def parse_type(self, response):
        '''
        获取每页五十个url
        :param response:
        :return:
        '''
        html = etree.HTML(response.text)
        type = response.meta['type']
        # if type == 'BLOG':
        #     divs = response.xpath('//div[@class="responsiveList"]/a')
        #     for div in divs:
        #         url_id = div.xpath('@href').extract_first()
        #         article_url = self.base_url + url_id
        #         title = div.xpath('@title').extract_first()
        #     # content_info = []
        #
        #         yield scrapy.Request(url=article_url, callback=self.parse_detail_page, meta={'title': title, 'type': type, 'article_url': article_url})
        #     next = response.xpath('//a[@class="pageNavNxA"]/@href').extract_first()
        #     if len(next) != 0:
        #         type = response.meta['type']
        #         next_url = self.base_url + next
        #         yield scrapy.Request(url=next_url, callback=self.parse_type, meta={'type': type})
        # if type == 'RESİM':
        #     divs = response.xpath('//div[@class="responsiveList"]/a')
        #     for div in divs:
        #         url_id = div.xpath('@href').extract_first()
        #         article_url = self.base_url + url_id
        #         title = div.xpath('@title').extract_first()
        #         yield scrapy.Request(url=article_url, callback=self.parse_detail_resim,
        #                              meta={'title': title, 'type': type, 'article_url': article_url})
        #     next = response.xpath('//a[@class="pageNavNxA"]/@href').extract_first()
        #     if len(next) != 0:
        #         type = response.meta['type']
        #         next_url = self.base_url + next
        #         yield scrapy.Request(url=next_url, callback=self.parse_type, meta={'type': type})
        if type == 'VİDEO':
            sections = response.xpath('//section[@class="responsiveList default"]/header/h1/a/@href').extract()
            for ur in sections:
                url = self.base_url + ur
                yield scrapy.Request(url=url, callback=self.parse_video,
                                     meta={'type': type})

    def parse_video(self, response):
        type = response.meta['type']
        html = etree.HTML(response.text)
        divs = response.xpath('//div[@class="responsiveList"]/a')
        for div in divs:
            url_id = div.xpath('@href').extract_first()
            article_url = self.base_url + url_id
            title = div.xpath('@title').extract_first()
            yield scrapy.Request(url=article_url, callback=self.parse_detail_video,
                                 meta={'title': title, 'type': type, 'article_url': article_url})
        next = response.xpath('//a[@class="pageNavNxA"]/@href').extract_first()

        if len(next) != 0:
            type = response.meta['type']
            next_url = self.base_url + next
            yield scrapy.Request(url=next_url, callback=self.parse_video, meta={'type': type})

    def parse_detail_page(self, response):
        '''
        访问解析每一个标题下面的回复：以及下一页回复
        :param response:
        :return:
        '''
        html = etree.HTML(response.text)
        # content_info = response.meta['content_info']
        div = html.xpath('//div[@class="articleBody"]')[1]
        publish_time = None
        title = response.meta['title']
        fonts = div.xpath('div//text()')
        content = ''
        scrawl_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for t in fonts:
            content += t
        article_url = response.meta['article_url']
        spider_type = '新闻'
        source = 'enteresan'
        type = response.meta['type']
        # print(content)
        # item = TuerqiItem()
        # item['title'] = title
        # item['content'] = content
        # item['article_url'] = article_url
        # item['spider_type'] = spider_type
        # item['publish_time'] = publish_time
        # item['scrawl_time'] = scrawl_time
        # item['source'] = source
        # item['type'] = type
        # yield item

    def parse_detail_resim(self, response):
        '''
        访问解析每一个标题下面的回复：以及下一页回复
        :param response:
        :return:
        '''
        html = etree.HTML(response.text)
        # content_info = response.meta['content_info']
        # div = html.xpath('//div[@class="articleBody"]')[1]
        publish_time = None
        title = response.meta['title']
        fonts = html.xpath('//div[@class="galleryImageDetail"]//text()')
        content = ''
        scrawl_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for t in fonts:
            content += t
        article_url = response.url
        print('++++++++++++++++++++++++++++++', article_url)
        # self.f.write(f'{article_url}\n')
        spider_type = '新闻'
        source = 'enteresan'
        type = response.meta['type']
        # # print(content)
        # item = TuerqiItem()
        # item['title'] = title
        # item['content'] = content
        # item['article_url'] = article_url
        # item['spider_type'] = spider_type
        # item['publish_time'] = publish_time
        # item['scrawl_time'] = scrawl_time
        # item['source'] = source
        # item['type'] = type
        # yield item
        next = response.xpath('//a[@class="navButton navButtonR"]/@href').extract_first()
        if len(next) != 0 and re.findall('page=', next):
            type = response.meta['type']
            title = response.meta['title']
            next_url = self.base_url + next
            yield scrapy.Request(url=next_url, callback=self.parse_detail_resim, meta={'type': type, 'title': title})

    def parse_detail_video(self, response):
        '''
        访问解析每一个标题下面的回复：以及下一页回复
        :param response:
        :return:
        '''
        html = etree.HTML(response.text)
        # content_info = response.meta['content_info']
        # div = html.xpath('//div[@class="articleBody"]')[1]
        publish_time = None
        title = response.meta['title']
        fonts = html.xpath('//div[@class="tc_11"]/text()')
        content = ''
        scrawl_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for t in fonts:
            content += t
        article_url = response.url
        print('++++++++++++++++++++++++++++++', article_url)
        # self.f.write(f'{article_url}\n')
        spider_type = '新闻'
        source = 'enteresan'
        type = response.meta['type']
        # print(content)
        item = TuerqiItem()
        item['title'] = title
        item['content'] = content
        item['article_url'] = article_url
        item['spider_type'] = spider_type
        item['publish_time'] = publish_time
        item['scrawl_time'] = scrawl_time
        item['source'] = source
        item['type'] = type
        yield item
        # next = response.xpath('//a[@class="navButton navButtonR"]/@href').extract_first()
        # if len(next) != 0 and re.findall('page=', next):
        #     type = response.meta['type']
        #     title = response.meta['title']
        #     next_url = self.base_url + next
        #     yield scrapy.Request(url=next_url, callback=self.parse_detail_resim, meta={'type': type, 'title': title})
