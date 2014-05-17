#!/usr/bin/env python

"A chat tool."

import sys
import socket
import threading
import Queue
import Tkinter
from time import sleep, ctime
from optparse import OptionParser, OptionGroup


CODEC = 'utf-8'
USERNUMBER = 5
RECVBUFFSIZE = 2048
USAGE = '%s [option] arg1, arg2' %(sys.argv[0],)
VERSION = 'v1.0'

class ChatThread(threading.Thread):
	"""docstring for ChatThread"""
	def __init__(self, founction, arg, name = ' '):
		super(ChatThread, self).__init__()
		self.founction = founction
		self.arg = arg
		self.name = name
		self.result = True

	def run(self):
		self.result = apply(self.founction, self.arg)

	def getResult(self):
		return self.result


def interfaceCL():
	parser = OptionParser(usage = USAGE, version = VERSION)

	parser.add_option('-v', '--verbose', action = 'store_true', \
	dest = 'verbose', help = 'output verbosely.', default = False)

	parser.add_option('-q', '--quiet', action = 'store_false', \
	dest = 'verbose', help = 'output quietly.', default = False)

	parser.add_option('-g', '--gui', action = 'store_true', \
	dest = 'gui', help = 'open the gui version.', default = False)

	(options, args) = parser.parse_args()

	return (options, args)


def getLocalIpAndPort():
#	localIp, localPort = raw_input('The local ip address and port:')
	localIp = raw_input('The local ip address:')
	localPort = raw_input('The local port:')

	return (str(localIp), int(localPort))


def getTargetIpAndPort():
#	targetIp, targetPort = raw_input('The target ip address and port:')
	targetIp = raw_input('\nThe target ip address:')
	targetPort = raw_input('The target port:')

	return (str(targetIp), int(targetPort))


def serverPrint(content):
	print '-----Begin to recvice-----\n'

	print '@[%s]Recive :%s\n' %(ctime(), content)
	

def localServer(me):
#	print '-----Begin to recvice-----'
	connect, yourAdd = me.accept()
	myLock = threading.Lock()

	myLock.acquire()

	content = connect.recv(RECVBUFFSIZE)

	while content:
		serverPrint(content)
		myLock.release()

		myLock.acquire()

		content = connect.recv(RECVBUFFSIZE)

	connect.close()


def clientPrint(totalBits):
	print '-----Begin to send-----\n'

	print u'@[%s]The bits size of your message :%s\n' \
	 %(ctime(), unicode(totalBits))


def localClient(you):
	myLock = threading.Lock()

	myLock.acquire()

	theWordToSend = raw_input('Enter :')

	totalBits = you.send(theWordToSend)

	while totalBits and theWordToSend != '$QUIT':
		clientPrint(totalBits)
		myLock.release()

		myLock.acquire()

		theWordToSend = raw_input('Enter :')
		if theWordToSend == '$QUIT':
			break

		totalBits = you.send(theWordToSend)


class ShiehChatWindow(object):
	"""docstring for ShiehChatWindow"""
	def __init__(self):
		super(ShiehChatWindow, self).__init__()
		self.top = Tkinter.Tk()
		self.top.title('SHIEHCHATGUI')
		self.top.maxsize(1000, 1000)
		self.top.minsize(500, 500)

		self.body = Tkinter.Frame(self.top, bg = 'black')
		self.body.pack(fill = 'both')

		self.label = Tkinter.Label(self.body, fg = 'white', \
			bg = 'black', text = 'Welcome To ShiehChat\'s GUI')
		self.label.pack()

		self.theWorldToSend = Tkinter.Entry(self.body)
		self.theWorldToSend.pack()

		self.top.mainloop()


def startChat():
	me = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	you = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	localIpAndPort = getLocalIpAndPort()
	targetIpAndPort = getTargetIpAndPort()

	me.bind(localIpAndPort)
	me.listen(USERNUMBER)

	you.connect(targetIpAndPort)

	#Create tread for sending and recivingg.
	meThread = ChatThread(localServer, arg = (me,))
	youThread = ChatThread(localClient, arg = (you,))

	#Start the shiehChat
	meThread.start()
	youThread.start()

	#Wait until all the tread has been finished.
	meThread.join()
	youThread.join()

	#Close the socket.
	me.close()
	you.close()


def main():
	options = interfaceCL()

	if options[0].gui:
		shiehChatWindow = ShiehChatWindow()
	else:
		startChat()

if __name__ == '__main__':
	main()
