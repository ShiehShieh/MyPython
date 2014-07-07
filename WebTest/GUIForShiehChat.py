##!/usr/bin/env python

import Tkinter

class ShiehChatWindow(object):
	"""docstring for ShiehChatWindow"""
	def __init__(self):
		super(ShiehChatWindow, self).__init__()
		self.top = Tkinter.Tk()
		self.top.title('SHIEHCHATGUI')
		self.top.minsize(500, 500)
#		self.top.maxsize(1000, 1000)

		self.body = Tkinter.Frame(self.top, bg = 'black')
		self.body.pack(fill = 'both')

		self.label = Tkinter.Label(self.body, fg = 'white', \
			bg = 'black', text = 'Welcome To ShiehChat\'s GUI')
		self.label.pack()

		self.theWorldToSend = Tkinter.Entry(self.body)
		self.theWorldToSend.pack()

		self.top.mainloop()


def main():
	shiehChat = ShiehChatWindow()


if __name__ == '__main__':
	main()