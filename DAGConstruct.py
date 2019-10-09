# -*- coding:utf-8 -*-

import pandas, re, csv

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

class GoTerm:
	term = ''
	par= []
	son = []
	def __init__(self, term='', par=[], son=[]):
		self.term = term
		self.par = par
		self.son = son

def getTerms():
	goTermDic = {}
	fcsv = pandas.read_csv('goTerms.csv', index_col = 0)
	# round one
	for index, row in fcsv.iterrows():
		if re.match('GO:[0-9]+', index) == None:
			continue
		goTerm = GoTerm(index, [], [])
		tree = []
		selfLevel = 0
		for term in row['TreeView'].split(' || '):
			nodeInfo = term.split(' // ')
			if re.match('GO:[0-9]+', nodeInfo[2]) == None:
				continue
			if nodeInfo[2] == index:
				selfLevel = int(nodeInfo[0])
			tree.append(GoNode(int(nodeInfo[0]), nodeInfo[1], nodeInfo[2], ''))
		for node in tree:
			if node.Level < selfLevel:
				goTerm.par.append(node.ID)
			elif node.Level > selfLevel:
				goTerm.son.append(node.ID)
		goTermDic[index] = goTerm
	# round two
	for key, value in goTermDic.items():
		for term in value.par:
			goTermDic[term].son.append(key)
		for term in value.son:
			if term in goTermDic:
				goTermDic[term].par.append(key)
	for key in goTermDic.keys():
		goTermDic[key].par = list(set(goTermDic[key].par))
		goTermDic[key].son = list(set(goTermDic[key].son))
	return goTermDic

if __name__ == '__main__':
	fcsv = open("GODAG.csv", "w", newline = '')
	fw = csv.writer(fcsv)
	fw.writerow(["term", "par", "son"])
	goTermDic = getTerms()
	for key, value in goTermDic.items():
		par = ''
		son = ''
		for term in value.par:
			if term == key:
				print('par error at', key)
			par += ' || ' + term
		for term in value.son:
			if term == key:
				print('son error at', key)
			son += ' || ' + term
		fw.writerow([key, par[4:], son[4:]])
	fcsv.close()
