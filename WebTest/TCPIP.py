#!/usr/bin/env python

import socket
import time

HOST = '192.168.1.103'
PORT = 22225
BUFSIZE = 1024
ADD = (HOST, PORT)

def main():
	sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sockets.bind(ADD)
	sockets.listen(5)

	while True:
		print "Waiting"
		tcpClient, addr = sockets.accept()

		print "connecting from:", addr
		while True:
			data = tcpClient.recv(BUFSIZE)

			if not data:
				break
			tcpClient.send("[%s] %s" %(time.ctime(), data))
		tcpClient.close()

	sockets.close()

if __name__ == '__main__':
	main()