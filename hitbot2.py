#!/usr/bin/env python
#
#   Title:  	Hit Bot 2
#   Author: 	Chris Shenkan
#   Date:  		5/7/2014
#   Version 	2.0.4
#

import requests
import datetime
from bs4 import BeautifulSoup
import time
import sys

def query_yes_no(question, default="yes"):
	"""Ask a yes/no question via raw_input() and return their answer.

	"question" is a string that is presented to the user.
	"default" is the presumed answer if the user just hits <Enter>.
		It must be "yes" (the default), "no" or None (meaning
		an answer is required of the user).

	The "answer" return value is one of "yes" or "no".
	"""
	valid = {"yes":True,   "y":True,  "ye":True,
			 "no":False,     "n":False}
	if default == None:
		prompt = " [y/n] "
	elif default == "yes":
		prompt = " [Y/n] "
	elif default == "no":
		prompt = " [y/N] "
	else:
		raise ValueError("invalid default answer: '%s'" % default)

	while True:
		sys.stdout.write(question + prompt)
		choice = raw_input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes' or 'no' "\
							 "(or 'y' or 'n').\n")

now = datetime.datetime.now()
currentDate = [str(now.month), str(now.day), str(now.year)]

url = "http://www.bostonfanfavorites.com"
host = url.replace("http://", "")
host = host.replace("https://", "")
host = host.replace("www.", "")
host = host.replace(".com", "")
host = host.replace(".net", "")
host = host.replace(".org", "")
textfile = host + "_scrape_" + "-".join(currentDate) + ".txt"

response = requests.get(url)

#urllist = []
#soup = (BeautifulSoup(response.content))
#for link in soup.find_all('a'):
#    urllist.append( link.get('href'))

# parse html
page = str(BeautifulSoup(response.content))


f = open(textfile, 'w')
goodurllist = []

def processURL(urlfile):
	"""
	:param urlfile: file of urls crawled from page in getURL(page)
	:return: status of success or failure
	"""
	with open(urlfile, 'r') as uf:
		for line in uf:
			r = requests.get(line)
			if (r.status_code == requests.codes.ok):
				line.append(goodurllist)
	for ab in goodurllist:
		print ab

def getURL(page):
	"""
	:param page: html of web page (here: Python home page) 
	:return: urls in that page 
	"""
	start_link = page.find("a href")
	if start_link == -1:
		return None, 0
	start_quote = page.find('"', start_link)
	end_quote = page.find('"', start_quote + 1)
	url = page[start_quote + 1: end_quote]
	return url, end_quote

while True:
	url, n = getURL(page)
	page = page[n:]
	if url:
		print url
		f.write(url)
		f.write("\n")
	else:
		print "Finished writing file."
		sys.exit(1)
