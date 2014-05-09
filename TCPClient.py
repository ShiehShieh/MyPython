#!/usr/bin/env python

import socket

HOST = '192.168.1.103'
PORT = 22225
BUFSIZE = 1024
ADD = (HOST, PORT)

def main():
	tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	tcpClient.connect(ADD)
	while True:
		data = raw_input(">")

		if not data:
			break
		tcpClient.send(data)
		data = tcpClient.recv(BUFSIZE)

		if not data:
			break
		print data

	tcpClient.close()

if __name__ == '__main__':
	main()