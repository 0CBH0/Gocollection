# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class GoNode:
	Level = 0
	Relation= ''
	ID = ''
	Description = ''
	def __init__(self, lv=0, rel='', id='', desc=''):
		self.Level = lv
		self.Relation = rel
		self.ID = id
		self.Description = desc

class GocollectionItem(scrapy.Item):
	# Primary fields
	Accession = scrapy.Field()
	Name = scrapy.Field()
	Ontology = scrapy.Field()
	Synonyms = scrapy.Field()
	Alternate_IDs = scrapy.Field()
	Definition = scrapy.Field()
	Comment = scrapy.Field()
	TreeView = scrapy.Field()
	
	# Info fields
	# Project = scrapy.Field()
	# Spider = scrapy.Field()
	# Server = scrapy.Field()
	URL = scrapy.Field()
	Date = scrapy.Field()
