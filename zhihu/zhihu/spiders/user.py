# -*- coding: utf-8 -*-
import scrapy
import json
from zhihu.items import UserItem


class UserSpider(scrapy.Spider):
	name = 'user'
	allowed_domains = ['www.zhihu.com']
	
	start_user = 'mileijun'
	
	user_url = ('https://www.zhihu.com/api/v4/members/{url_token}?'
				'include=allow_message%2Cis_followed%2Cis_following'
				'%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count'
				'%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge'
				'%5B%3F(type%3Dbest_answerer)%5D.topics')
	
	followers_url = ('https://www.zhihu.com/api/v4/members/{url_token}/followers?'
					'include=data%5B*%5D.answer_count%2Carticles_count%2Cgender'
					'%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F'
					'(type%3Dbest_answerer)%5D.topics&offset=0&limit=20')
	
	followees_url = ('https://www.zhihu.com/api/v4/members/{url_token}/followees?'
					'include=data%5B*%5D.answer_count%2Carticles_count%2Cgender'
					'%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F'
					'(type%3Dbest_answerer)%5D.topics&offset=0&limit=20')
	
	def start_requests(self):
		yield scrapy.Request(self.user_url.format(url_token=self.start_user), callback=self.parse_user)
		yield scrapy.Request(self.followers_url.format(url_token=self.start_user), callback=self.parse_followers)
		yield scrapy.Request(self.followees_url.format(url_token=self.start_user), callback=self.parse_followees)
	
	
	def parse_user(self, response):
		results = json.loads(response.text)
		item = UserItem()
		for field in item.fields:
			if field in results.keys():
				item[field] = results.get(field)
				
		yield item    # 调用 process_item
		yield scrapy.Request(self.followers_url.format(url_token=results.get('url_token')), callback=self.parse_followers)
		yield scrapy.Request(self.followees_url.format(url_token=results.get('url_token')), callback=self.parse_followees)
		
	def parse_followers(self, response):
		results = json.loads(response.text)
		if 'data' in results.keys():
			for user in results.get('data'):
				yield scrapy.Request(self.user_url.format(url_token=user.get('url_token')), callback=self.parse_user)
				
		if 'paging' in results.keys() and results.get('is_end') == False:
				yield scrapy.Request(results.get('paging').get('next'), callback=self.parse_followers)
				

	def parse_followees(self, response):
		results = json.loads(response.text)
		if 'data' in results.keys():
			for user in results.get('data'):
				yield scrapy.Request(self.user_url.format(url_token=user.get('url_token')), callback=self.parse_user)
				
		if 'paging' in results.keys() and results.get('is_end') == False:
				yield scrapy.Request(results.get('paging').get('next'), callback=self.parse_followees)
		
		
		
		
		
		
		
		
		
		
		
		
		
