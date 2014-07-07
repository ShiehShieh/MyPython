#/usr/bin/ python

import os, time

def compileCpp(fileName):
	"A Founction used to complile your Cpp source file on Unix."
	print "Going to complile your cpp file:" + fileName + ".cpp"
	time.sleep(1)
	os.system("g++ -std=c++11 "+fileName+".cpp"+" -o "+fileName)
	return fileName

def run(fileName):
	"A Founction used to run your executable file on Unix."
	print "Going to run your Cpp programme." + fileName
	time.sleep(1)
	runFileName = "./"+fileName
	os.system(runFileName)

def main():
	"The main founction."
	files = (raw_input("All of your files:").split(" "))
	filenumber = len(files)
	count = 0
	while count<filenumber:
		rFileName = compileCpp(files[count])
		run(rFileName)
		count += 1
		time.sleep(2)
	else:
		count = 0

if __name__ == '__main__':
	main()