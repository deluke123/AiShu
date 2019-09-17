# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class TuerqiPipeline(object):

    def __init__(self):
        self.username = 'new_news'
        self.password = 'magic_123'
        # self.client = pymongo.MongoClient(host='39.105.138.234', port=27017)
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        db = self.client.xinwen_DB
        db.authenticate(self.username, self.password)
        self.collection = db.tuerqi_enteresan

    def process_item(self, item, spider):
        travell_dic = dict(item)
        self.collection.insert_one(travell_dic)
