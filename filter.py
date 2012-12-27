#!/usr/bin/pyhon	

import urllib
import sys
import re
from sets import Set
from time import gmtime, strftime
import glob

newFile = ''
oldFiles = []
#global filePath

def isGoodLink(url):
#Use rules to determine whether a link should be considered for manual reviewing
	content = urllib.urlopen(url).read()
	isExpired = False
#	isGMap = False
	for line in content.splitlines():
		title_match = re.search('<h2>This posting has been flagged for removal', line)
	#Remove expired links
		if (title_match):
			isExpired = True
			break
#		map_match = re.search('google map', line)
#		if (map_match):
#			isGMap = True
#			break
#	if (not isExpired) & isGMap:
	if not isExpired:
		return True
	else:
		return False

def loadLinks():
	#Load all unique titles
	#Mark links that gone bad 
	nCount = 0
	titles = Set([])
	badLinks = ''
	goodLinks = ''
	for filePath in oldFiles:
		print filePath
		try:
			f = open(filePath, 'r+')
		except:
			print 'File does not exsist, creating a new file'
			return titles
		for line in f.readlines():
			nCount += 1
			ar = line.split('\t')
			if (len(ar) != 6):
				print 'Error while parsing line: ' + line
			title = ar[5].strip('\n')
			if ar[1] == 'Good':
				if isGoodLink(ar[3]):
					titles.add(title)
					goodLinks += line
				else:
					badLinks += line
			else:
				badLinks += line
		f.close()
		#Write all good and bad links to the file.
		f = open(filePath, 'w')
		f.write(goodLinks)
		f.write(badLinks)
		goodLinks = ''
		badLinks = ''
		f.close()
	print len(titles)
	return titles

def fetchLinks(url, nBed, titles, count):
#Crawl housing rental links from craigslist then return all of potential links
	content = urllib.urlopen(url).read()
	link = ''
	title = ''
	latitude = ''
	longtitude = ''	
	beds = 0
	price = ''
	#open file for append
	f = open(newFile, 'a+')
	badLinks = ''
	for line in content.splitlines():
		match_link = re.search('^ *<a href="(http://newyork\.craigslist\.org.*?)">(.*?)</a>', line)
		if (match_link):
			link = match_link.group(1)
			title = match_link.group(2)
		else:
			match_info = re.search('<span class="itemph">\$(.*?) / (.)br(.*?)</span>', line)
			if(match_info):
				beds = int(match_info.group(2))
				price = match_info.group(1)
			else:
				match_loc = re.search('<span class="itempn"><font size="-1"> (\(.*?\))</font></span>', line)
				if match_loc:
					if (beds == nBed):
						if (title not in titles):
							count += 1
							if (isGoodLink(link)):
								aGoodLink = str(count) + '\tGood\t' +  price + '\t' + link + '\t' + match_loc.group(1).lower() + '\t' + title + '\n'
								f.write(aGoodLink)
								titles.add(title) #todo
							else:
								badLinks += str(count) + '\tBad\t' + price + '\t' + link + '\t' + match_loc.group(1).lower() + '\t' + title + '\n'
	
		#Get location
	f.write(badLinks)
	f.close()
	#return links
	print 'length = ' + str(len(titles))
	return count
	

def main(argv):
	nBed = int(argv[0])
	maxP = 800*nBed
	minP = 600*nBed
	global oldFiles
	global newFile
	oldFiles = glob.glob('links_' + argv[0] + '*')
	newFile  = 'links_' + argv[0] + '_' + strftime("%Y-%m-%d--%H:%M:%S", gmtime()) + '.cvs'
	category = ['abo']
	#first 100 links
	titles = loadLinks()
	url100 = 'http://newyork.craigslist.org/search/hhh/brk?sort=date&bedrooms=' + argv[0] + '&hasPic=1&maxAsk=' + str(maxP) + '&minAsk=' + str(minP) + '&srchType=A'
	count = fetchLinks(url100, nBed, titles, 0)
	#next links
	for i in range(1, 10):
		index = str(i*100)
		url = 'http://newyork.craigslist.org/search/hhh/brk?sort=date&bedrooms=' + argv[0] + '&hasPic=1&maxAsk=' + str(maxP) + '&minAsk=' + str(minP) + '&srchType=A&s=' + index
		count = fetchLinks(url, nBed, titles, count)
if __name__ == "__main__":
	main(sys.argv[1:])
