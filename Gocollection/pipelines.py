# -*- coding: utf-8 -*-

from scrapy import signals
import sqlite3
import time
import re

class Sqlite3Pipeline(object):

	def __init__(self, update_time, sqlite_file, sqlite_table):
		self.update_time = update_time
		self.sqlite_file = sqlite_file
		self.sqlite_table = sqlite_table

	@classmethod
	def from_crawler(cls, crawler):
		return cls(update_time = crawler.settings.get('UPDATE_TIME'), sqlite_file = crawler.settings.get('SQLITE_FILE'), sqlite_table = crawler.settings.get('SQLITE_TABLE', 'items'))

	def open_spider(self, spider):
		self.conn = sqlite3.connect(self.sqlite_file)
		self.cur = self.conn.cursor()

	def close_spider(self, spider):
		self.cur.close()
		self.conn.close()

	def process_item(self, item, spider):
		result = ''
		select_sql = 'SELECT Date FROM {0} WHERE Accession == \'{1}\''.format(self.sqlite_table, item['Accession'])
		self.cur.execute(select_sql)
		res = self.cur.fetchall()
		if len(res) == 0:
			for term in item.fields.keys():
				result += ', ' + '\'' + item[term].replace('\'', '\'\'') + '\''
			result = result[2:]
			insert_sql = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(self.sqlite_table, ', '.join(item.fields.keys()), result)
			self.cur.execute(insert_sql)
			self.conn.commit()
		else:
			time_ori = time.mktime(time.strptime(res[0][0].encode('utf-8','replace'), "%Y-%m-%d %H:%M:%S"))
			time_new = time.mktime(time.strptime(item['Date'], "%Y-%m-%d %H:%M:%S"))
			if time_new - time_ori > self.update_time:
				for term in item.fields.keys():
					if term == 'Accession':
						continue
					update_sql = "UPDATE {0} SET {1} = \'{2}\' WHERE Accession == \'{3}\'".format(self.sqlite_table, term, item[term], item['Accession'])
					self.cur.execute(update_sql)
					self.conn.commit()
		return item
