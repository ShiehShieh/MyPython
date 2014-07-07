#!/usr/bin/env python

"""This is a tiny document-statistic module. You can use it to search your directory."""

import sys, os

CODEC = 'utf-8'
TIMES = 0

class SingleFile(object):
	"""docstring for SingleFile"""
	def __init__(self, arg):
		super(SingleFile, self).__init__()
		self.arg = arg		

class Directory(object):
	"""docstring for Directory"""
	def __init__(self, arg):
		super(Directory, self).__init__()
		self.arg = arg

def fFilePath():
	global TIMES, CODEC
	fileSize = 0
	outFileName = "output"
	mod = raw_input("Please select a module : ")

	while mod != 'quit':
		try:

			#choose your module.
			if mod == "manual":
				userInputFile = raw_input("Please enter your file path : ")
				filePath = os.path.dirname(userInputFile)
			elif mod == "default":
				filePath = os.path.dirname(__file__)
			else :
				raise RuntimeError("No such command.\nPlease try again.")

			allFile = os.listdir(filePath)
			for each in allFile:
				fileSize += os.path.getsize(each)
			print fileSize

			#output.
			TIMES += 1
			outPutFile = open(outFileName + str(TIMES) + ".txt", 'w')

			#sort the files according to lambda
			allFile = sorted(allFile, cmp = lambda x, y: os.path.getsize(x) - os.path.getsize(y))

			#write to file.
			for files in allFile:
				outPutFile.writelines(files + ' : ' + str(os.path.getsize(files)) + '\n')

			outPutFile.close()
		except RuntimeError, e:
			print e

		#again.
		mod = raw_input("Please select a module : ")

def main():
	fFilePath()

if __name__ == '__main__':
	main()