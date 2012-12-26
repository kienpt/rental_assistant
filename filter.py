#!/usr/bin/pyhon	

import urllib
import sys
import re
from sets import Set

filePath = './links.csv'
#global filePath

def isGoodLink(url):
#Use rules to determine whether a link should be considered for manual reviewing
	content = urllib.urlopen(url).read()
	
	for line in content:
		title_match = re.search('<h2>This posting has been flagged for removal', line)
	#Remove expired links
		if (title_match):
			return False
	return True

def loadLinks():
	nCount = 0
	titles = Set([])
#	links = []
	try:
		f = open(filePath, 'r+')
	except:
		print 'It seems file does not exsisted'
#		return (titles, links)
		return titles
	for line in f.readlines():
		nCount += 1
		print nCount
		ar = line.split('\t')
		if (len(ar) != 5):
			print 'Error while parsing line: ' + line
		title = ar[4].strip('\n')
		if isGoodLink(ar[1]):
			titles.add(title)
#		links.append(line)	
	content = f.read().split('\n')
	f.close()
#	return (titles, links)
	return titles

def fetchLinks(url, nBed):
#Crawl housing rental links from craigslist then return all of potential links
	count_all = 0
#	links = []
#	unqTitles = Set([])	
#	unqTitles, links = loadLinks()
	unqTitles = loadLinks()
	content = urllib.urlopen(url).read()
	link = ''
	title = ''
	latitude = ''
	longtitude = ''	
	f = open(filePath, 'a+')
	for line in content.splitlines():
#		<p class="row" data-latitude="40.6812639592492" data-longitude="-73.928744301753">
		match_pos = re.search('<p class="row" data\-latitude="(.*?)" data\-longitude="(.*?)">', line)
		if(match_pos):
			latitude = match_pos.group(1)
			longtitude = match_pos.group(2)
		else:
			match_link = re.search('^ *<a href="(http://newyork\.craigslist\.org.*?)">(.*?)</a>', line)
			if (match_link):
				count_all = count_all + 1
				link = match_link.group(1)
				title = match_link.group(2)
			else:
				match_info = re.search('<span class="itemph">\$(.*?) / (.)br(.*?)</span>', line)
				if(match_info):
					if (int(match_info.group(2)) == nBed):
						if latitude == '':
							latitude = '0000000000000000'
							longtitude = '0000000000000000'
						if (title not in unqTitles) & (isGoodLink(link)):
							aLink =  match_info.group(1) + '\t' + link + '\t' + latitude + '\t' + longtitude + '\t' + title + '\n'
							f.write(aLink)
							unqTitles.add(title) #todo
	f.close()
	#return links
	print len(unqTitles)

	

def main(argv):
	nBed = int(argv[0])
	maxP = 800*nBed
	minP = 600*nBed
	global filePath
	filePath = './links_' + argv[0] + '.cvs'
	category = ['abo']
	#first 100 links
	url100 = 'http://newyork.craigslist.org/search/hhh/brk?sort=date&bedrooms=' + argv[0] + '&hasPic=1&maxAsk=' + str(maxP) + '&minAsk=' + str(minP) + '&srchType=A'
	fetchLinks(url100, nBed)
	#next links
	for i in range(1, 10):
		index = str(i*100)
		url = 'http://newyork.craigslist.org/search/hhh/brk?sort=date&bedrooms=' + argv[0] + '&hasPic=1&maxAsk=' + str(maxP) + '&minAsk=' + str(minP) + '&srchType=A&s=' + index
		fetchLinks(url, nBed)
if __name__ == "__main__":
	main(sys.argv[1:])
