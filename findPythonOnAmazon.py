#!/usr/bin/env python

"My tiny application which help me to pull down the data I need."

from splinter import Browser
import re

CODEC = 'utf-8'

def openBrower():
	browser = Browser('chrome')
	browser.visit('https://www.amazon.cn/gp/switch-language/homepage.html/ref=topnav_switchLang?ie=UTF8&language=en_CN')
	browser.fill('field-keywords', 'Python')
	browser.find_by_value('Go').check()

	return browser

def quitBrowser(browser):
	browser.quit()

def outputData(myElement):
	outFile = open('webDataoutput.xie', 'a')
	outFile.write(myElement.value.encode(CODEC))
	outFile.close()

#find the data match the regular expression.
def findData(browser):
	for i in xrange(0,25):
		myElementList = browser.find_by_id(u'result_' + unicode(i))

		for myElement in myElementList:
			spanList = myElement.find_by_tag('span')

			for span in spanList:
				reData = re.search('(.*)python(.*)|(.*)Python(.*)', span.value)

				if reData is not None:

					#output the data to the external file.
					outputData(myElement)
				else:
					print unicode(span.value) + ' Not match.'

def main():
	#recvice the browser.
	browser = openBrower()

	#find the data in need.
	while raw_input('order : ') != 'quit':
		findData(browser)

	#quit the application.
	quitBrowser(browser)

if __name__ == '__main__':
	main()