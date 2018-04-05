# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

class ZhihuPipeline(object):

	host = settings.get('MONGODB_HOST')
	port = settings.get('MONGODB_PORT')
	db = settings.get('MONGODB_DB')
	sheet = settings.get('MONGODB_SHEET')

	client = pymongo.MongoClient(host=host, port=port)
	zhihu = client[db]
	user = zhihu[sheet]

	def process_item(self, item, spider):
		self.user.update({'url_token':item["url_token"]},{'$set':item},True)
		return item
