# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import datetime


class TravelPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        db = self.client.luntan_DB
        self.collection = db.travellerspoint

    def process_item(self, item, spider):
        travell_dic = dict(item)
        self.collection.insert_one(travell_dic)
