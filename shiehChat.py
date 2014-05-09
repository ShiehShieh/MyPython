#!/usr/bin/env python

"A chat tool."

import socket
import threading
import Queue
from time import sleep, ctime

CODEC = 'utf-8'
USERNUMBER = 5
RECVBUFFSIZE = 2048

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

	print '@[%s]Recive:%s\n' %(ctime(), content)
	

def localServer(me):
#	print '-----Begin to recvice-----'

	connect, yourAdd = me.accept()

	content = connect.recv(RECVBUFFSIZE)

	while content:
		serverPrint(content)

		content = connect.recv(RECVBUFFSIZE)

	connect.close()


def clientPrint(totalBits):
	print '-----Begin to send-----\n'

	print u'@[%s]The bits size of your message:%s\n' \
	 %(ctime(), unicode(totalBits))


def localClient(you):
	theWorldToSend = raw_input()

	totalBits = you.send(theWorldToSend)

	while totalBits:
		clientPrint(totalBits)

		theWorldToSend = raw_input()
		if theWorldToSend == '$QUIT':
			break

		totalBits = you.send(theWorldToSend)


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


def run():
	startChat()


def main():
	run()


if __name__ == '__main__':
	main()