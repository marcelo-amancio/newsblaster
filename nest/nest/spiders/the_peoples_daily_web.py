import scrapy
import re
from datetime import datetime
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from nest.items import ArticleItem, ArticleMetaInformation
from scrapy.selector import Selector

#TODO implement throttle

class PeopleDailySpiderWeb(CrawlSpider):

	name = "the_peoples_daily_web"
	download_delay = 2
	allowed_domains = ["english.people.com.cn"]

	start_urls = (
			'http://english.people.com.cn/',
		     )		


	#Follow only these specific links
	article_link_format = re.compile('http://english.people.com.cn/n/\d+/\d+')

	#Rules to handle following urls
	rules = (Rule(LxmlLinkExtractor(allow=(article_link_format), allow_domains=('english.people.com.cn', )),callback='parse_follow',follow=True), )

	def parse_follow(self, response):

		article_item = ArticleItem()
		article_meta_information = ArticleMetaInformation()

		article_item['source_link'] = response.url
		article_item['time_of_crawl'] = int(datetime.strptime(response.headers['Date'],"%a, %d %b %Y %H:%M:%S %Z").strftime("%s"))*1000
		article_item['html_content'] = response.body
		article_item['source_type'] = 'news_article' #TODO  should be enum
		
		article_item['title'] = response.xpath('//title/text()').extract()

		published_date = response.xpath('//meta[@name=\'publishdate\']/@content').extract()
		article_meta_information['date_published'] = int(datetime.strptime(published_date[0],"%Y-%m-%d").strftime("%s"))*1000
		article_meta_information['location'] = 'china' #TODO should be enum

		if response.xpath('//div[contains(@class, "wb_4 clear")]/text()').re(r'Editor:\s*(.*)'):
			raw_authors = response.xpath('//div[contains(@class, "wb_4 clear")]/text()').re(r'Editor:\s*(.*)')
			article_meta_information['author'] = self.get_authors(raw_authors)
		else:
			raw_authors = response.xpath('//div[contains(@class, "wb_13 clear")]/text()').re(r'Editor:\s*(.*)')
			article_meta_information['author'] = self.get_authors(raw_authors)


		keywords = response.xpath('//meta[@name=\'keywords\']/@content').extract()
		article_meta_information['topics'] = self.get_topics(keywords)
		article_meta_information['language'] = 'zh' #http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
		article_item['meta_information'] = article_meta_information
		return article_item
	
	def get_topics(self,keywords):
		
		#data always present in 0 of array
		for keyword_list in keywords:
			return keyword_list.split(',')


	def get_authors(self,raw_authors):
		return  [raw_author for raw_author in raw_authors]  #TODO Encoding for raw author
