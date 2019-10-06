 # -*- coding: utf-8 -*-
import scrapy
import time
import re
import socket
from scrapy.http import Request
from scrapy.loader import ItemLoader
from Gocollection.items import GoNode
from Gocollection.items import GocollectionItem

class TestSpider(scrapy.Spider):
	name = 'test'
	crawled_urls = set()
	#start_urls = ['http://amigo.geneontology.org/amigo/term/GO:0008562',]
	start_urls = ['http://amigo.geneontology.org/amigo/term/GO:0000904',]

	def parse(self, response):
		term = ItemLoader(item = GocollectionItem(), response = response)
		
		# Primary fields
		ddList = response.xpath('//dl[contains(@class, "amigo-detail-info")]')
		ddList = ddList.xpath('./dt | ./dd')
		ddInfo = ''
		ddDic = {}
		for dd in ddList:
			ddType = dd.xpath('name()').get().strip().encode('utf-8','replace')
			if ddType == 'dt':
				ddInfo = dd.xpath('./text()').get().strip().encode('utf-8','replace').replace(' ', '_')
				ddDic[ddInfo] = []
			elif ddType == 'dd':
				ddData = ''
				ddDataList = dd.xpath('.//text()').getall()
				if ddDataList != None:
					for d in ddDataList:
						ddData += d.strip().encode('utf-8','replace')
				ddDic[ddInfo].append(ddData)
		for info in ddDic.keys():
			if info in term.item.fields:
				term.item[info] = ''
				itemInfoList = ddDic[info]
				if len(itemInfoList) > 0:
					term.item[info] = itemInfoList[0]
					for i in range(len(itemInfoList) - 1):
						term.item[info] += ' || ' + itemInfoList[i + 1]
		if 'Comment' in ddDic:
			for i in ddDic['Comment']:
				addTerm = re.findall('.*replaced by:.*?(GO:[0-9]+)', i)
				if len(addTerm) > 0:
					url = 'http://amigo.geneontology.org/amigo/term/' + addTerm[0]
					self.log(url)
		tree = []
		levelList = []
		termLevel = 0
		for level in response.xpath('//div[@id="display-lineage-tab"]//ul[@class="list-unstyled"]/comment()').re('number_of_spaces.*?([0-9]+)'):
			levelList.append(int(level.strip().encode('utf-8','replace')))
		li = response.xpath('//div[@id="display-lineage-tab"]//ul[@class="list-unstyled"]/li')
		if len(li) == len(levelList):
			for index in range(len(levelList)):
				liTest = li[index].xpath('./a/text()')
				if len(liTest) == 0:
					liTest = li[index].xpath('./span/text()')
				nodeInfo = liTest.get().encode('utf-8','replace').split('\xc2\xa0', 1)
				nodeInfo.append(li[index].xpath('./img/@title').get().encode('utf-8','replace'))
				if nodeInfo[0] == term.item['Accession']:
					termLevel = levelList[index]
				tree.append(GoNode(levelList[index], nodeInfo[2], nodeInfo[0], nodeInfo[1]))
		term.item['TreeView'] = ''
		if len(tree) > 0:
			term.item['TreeView'] = str(tree[0].Level) + ' // ' + tree[0].Relation + ' // ' + tree[0].ID
			for i in range(len(tree) - 1):
				term.item['TreeView'] += ' || ' + str(tree[i + 1].Level) + ' // ' + tree[i + 1].Relation + ' // ' + tree[i + 1].ID
			for i in range(len(tree)):
				if tree[i].Level >= termLevel:
					break
				url = 'http://amigo.geneontology.org/amigo/term/' + tree[i].ID
				self.log(url)
		
		# Info fields
		term.item['URL'] = response.url
		# term.add_value('Project', self.settings.get('BOT_NAME'))
		# term.add_value('Spider', self.name)
		# term.add_value('Server', socket.gethostname())
		term.item['Date'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
		yield term.load_item()
