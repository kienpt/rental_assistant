#!/usr/bin/python

import urllib
import sys
import re

def main(argv):
	nBed = int(argv[0])
	maxP = 800*nBed
	minP = 600*nBed
	count_all = 0
	category = ['abo']
	url100 = 'http://newyork.craigslist.org/search/hhh/brk?sort=date&bedrooms=' + argv[0] + '&hasPic=1&maxAsk=' + str(maxP) + '&minAsk=' + str(minP) + '&srchType=A'
	content = urllib.urlopen(url100).read()
	link = ''
	title = ''
	latitude = ''
	longtitude = ''	
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
						print match_info.group(1) + '\t' + link + '\t' + title + '\t' + latitude + '\t' + longtitude

if __name__ == "__main__":
	main(sys.argv[1:])
