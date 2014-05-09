#!/usr/bin/env python

import sys
from optparse import OptionParser

USAGE = 'usage: %s [option] arg1, arg2' %(sys.argv[0])

def interface():
	optionParser = OptionParser(usage = USAGE)

	optionParser.add_option('-v', '--verbose', \
		help = "output verbosely", action = 'store_true',\
		dest = 'verbose')

	(options, args) = optionParser.parse_args()

def main():
	interface()

if __name__ == '__main__':
	main()