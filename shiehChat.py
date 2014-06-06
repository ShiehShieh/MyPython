#!/usr/bin/env python

"A chat tool."

import re
import os
import sys
import socket
import threading
import Queue
import Tkinter
from time import sleep, ctime
from optparse import OptionParser, OptionGroup


CODEC        = 'utf-8'
USERNUMBER   = 5
RECVBUFFSIZE = 2048
USAGE        = '%s [option] arg1, arg2' %(sys.argv[0],)
VERSION      = 'v1.0'

class ChatThread(threading.Thread):
    """docstring for ChatThread"""
    def __init__(self, founction, arg, name = ' '):
        super(ChatThread, self).__init__()
        self.founction = founction
        self.arg       = arg
        self.name      = name
        self.result    = True

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
#   localIp, localPort = raw_input('The local ip address and port:')
    localIp            = raw_input('The local ip address:')
    localPort          = raw_input('The local port:')

    return (str(localIp), int(localPort))


def getTargetIpAndPort():
#   targetIp, targetPort = raw_input('The target ip address and port:')
    targetIp             = raw_input('\nThe target ip address:')
    targetPort           = raw_input('The target port:')

    return (str(targetIp), int(targetPort))


def serverPrint(content):
    print '\033[0;34;1m-----Begin to recvice-----\n\033[0m'

    print '@[%s]Recive :%s\n' %(ctime(), content)
    

def localServer(me):
#   print '-----Begin to recvice-----'
    connect, yourAdd = me.accept()
    myLock           = threading.Lock()

    myLock.acquire()

    content = connect.recv(RECVBUFFSIZE)

    while content:
        if len(content) > 100:
#            indexs = content.find('#')
#            os.system('open %s' % (content[indexs + 1 : ],))
            with open('downloadFile.png', 'w') as downloadFile:
                downloadFile.write(content)
#            serverPrint(content[ : indexs])
            myLock.release()

            myLock.acquire()

            content = connect.recv(RECVBUFFSIZE)

            continue

        serverPrint(content)
        myLock.release()

        myLock.acquire()

        content = connect.recv(RECVBUFFSIZE)

    connect.close()


def clientPrint(totalBits):
    print '\033[0;34;1m-----Begin to send-----\n\033[0m'

    print u'@[%s]The bits size of your message :%s\n' \
     %(ctime(), unicode(totalBits))


def fileOpen(theWordToSend, you):
    """@todo: Docstring for function.

    :arg1: @todo
    :returns: @todo

    """
    if theWordToSend[0] == '/' :
        with open(theWordToSend, 'r') as fileToSend:
            fileContent = fileToSend.read()
            you.send(fileContent)

        return True
    else:
        return False



def localClient(you):
    myLock = threading.Lock()

    myLock.acquire()

    theWordToSend = raw_input('Enter :')

    if fileOpen(theWordToSend, you):
        totalBits = 1
    else:
        totalBits = you.send(theWordToSend)

    while totalBits and theWordToSend != '$QUIT':
        clientPrint(totalBits)
        myLock.release()

        myLock.acquire()

        theWordToSend = raw_input('Enter :')
        if theWordToSend == '$QUIT':
            break

        if fileOpen(theWordToSend, you):
            totalBits = 1
        else:
            totalBits = you.send(theWordToSend)


class ShiehChatWindow(object):
    """docstring for ShiehChatWindow"""
    def __init__(self, you, me):
        super(ShiehChatWindow, self).__init__()
        self.you = you
        self.me  = me

        self.top = Tkinter.Tk()
        self.top.title('SHIEHCHATGUI')
        self.top.maxsize(1000, 1000)
        self.top.minsize(500, 500)
        self.top.geometry('800x800')

        self.logging = Tkinter.StringVar(self.top)

        self.body = Tkinter.Frame(self.top, bg = 'black')
        self.body.pack(fill = 'both', expand = 1, side = 'left')

        self.userInput  = Tkinter.StringVar(self.body)
        self.userRecive = Tkinter.StringVar(self.body)

        self.label = Tkinter.Label(self.body, fg = 'white', \
            bg = 'black', text = 'Welcome To ShiehChat\'s GUI')
        self.label.pack()

        self.theWorldToSend = Tkinter.Entry(self.body, \
            textvariable = self.userInput)
        self.theWorldToSend.bind("<Key-Return>", self.sendMessage)
        self.theWorldToSend.pack()

        self.quitB = Tkinter.Button(self.body, text = 'QUIT', \
            bg = 'black', command = self.top.quit)
        self.quitB.pack(side = 'bottom')

        self.button = Tkinter.Button(self.body, text = 'SUBMIT', \
            bg = 'black')
        self.button.bind("<Button>", self.sendMessage)
        self.button.pack(side = 'bottom')

        self.log = Tkinter.Message(self.body, fg = 'white', \
            bg = 'black', bd = '25px', \
            textvariable = self.userRecive)
        self.log.pack(fill = 'both', expand = 1)

        self.navigationBar = Tkinter.Frame(self.top, bg = 'black')
        self.navigationBar.pack(side = 'right')

        self.infoBar = Tkinter.Scale(self.navigationBar, \
            from_ = 0, to_ = 50, \
            command = self.location)
        self.infoBar.set(1)
        self.infoBar.pack(side = 'right')

        meThread = ChatThread(self.reciveMessage, arg = ())
        meThread.start()

        self.top.mainloop()

    def printUserInput(self, event):
        print self.userInput.get()

    def returnUserInput(self):
        return self.userInput

    def location(self, event):
        if (self.infoBar.get() // 50) * len(self.logging.get()) < 5:
            begin = (self.infoBar.get() // 50) * len(self.logging.get())
        else :
            begin = (self.infoBar.get() // 50) * len(self.logging.get()) - 5

        if (self.infoBar.get() // 50) * len(self.logging.get()) > len(self.logging.get()) - 5:
            end = (self.infoBar.get() // 50) * len(self.logging.get()) + 1
        else :
            end = (self.infoBar.get() // 50) * len(self.logging.get()) + 5

        self.userRecive.set('\n'.join(re.split('\W+', \
            self.logging.get())[begin : end]))

    def sendMessage(self, event):
        myLock = threading.Lock()

        myLock.acquire()

        theWordToSend = self.userInput.get()

        totalBits = self.you.send(theWordToSend)

        if totalBits and theWordToSend != '$QUIT':
            clientPrint(totalBits)
            myLock.release()

    def reciveMessage(self):
        connect, yourAdd = self.me.accept()
        myLock = threading.Lock()

        myLock.acquire()

        content = connect.recv(RECVBUFFSIZE)

        while content:
            self.logging.set(self.logging.get() + content + '::')
            self.userRecive.set(self.userRecive.get() + \
                content + '\n')

            serverPrint(content)
            myLock.release()

            myLock.acquire()

            content = connect.recv(RECVBUFFSIZE)

        connect.close()


def startChat():
    me  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    you = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    localIpAndPort  = getLocalIpAndPort()
    targetIpAndPort = getTargetIpAndPort()

    me.bind(localIpAndPort)
    me.listen(USERNUMBER)

    you.connect(targetIpAndPort)

    #Create tread for sending and recivingg.
    meThread  = ChatThread(localServer, arg = (me,))
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


class GUIIPGetting(object):
    """docstring for GUIIPGetting"""
    def __init__(self, localIpAndPort, targetIpAndPort):
        super(GUIIPGetting, self).__init__()
        self.localIpAndPort  = localIpAndPort
        self.targetIpAndPort = targetIpAndPort

        self.top = Tkinter.Tk()
        self.top.title("IPAddress Required.")
        self.top.geometry('500x500')

        self.body           = Tkinter.Frame(self.top, bg   = 'black')
        self.body.pack(fill = 'both', expand               = 1)
        self.localIP        = Tkinter.StringVar(self.body)
        self.localPORT      = Tkinter.IntVar(self.body)
        self.targetIP       = Tkinter.StringVar(self.body)
        self.targetPORT     = Tkinter.IntVar(self.body)

        self.serverHost = Tkinter.Entry(self.body, bg = 'black', \
            fg = 'white', textvariable = self.localIP)
        self.serverHost.pack()
        self.serverPort = Tkinter.Entry(self.body, bg = 'black', \
            fg = 'white', textvariable = self.localPORT)
        self.serverPort.pack()
        self.clientHost = Tkinter.Entry(self.body, bg = 'black', \
            fg = 'white', textvariable = self.targetIP)
        self.clientHost.pack()
        self.clientPort = Tkinter.Entry(self.body, bg = 'black', \
            fg = 'white', textvariable = self.targetPORT)
        self.clientPort.bind('<Key-Return>', self.returnIPPORT)
        self.clientPort.pack()

        self.quit = Tkinter.Button(self.body, text = 'QUIT', \
            command = self.top.quit)
        self.quit.pack(side = 'bottom')
        self.sumbit = Tkinter.Button(self.body, text = 'SUBMIT', \
            command = self.returnIPPORT)
        self.sumbit.pack(side = 'bottom')

        self.top.mainloop()

    def returnIPPORT(self, event):
        self.localIpAndPort.append(self.localIP.get())
        self.localIpAndPort.append(self.localPORT.get())
        self.targetIpAndPort.append(self.targetIP.get())
        self.targetIpAndPort.append(self.targetPORT.get())

        self.top.destroy()


def startChatGUI():
    you = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    me  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    localIpAndPort  = []
    targetIpAndPort = []
    addressObject   = GUIIPGetting(localIpAndPort, targetIpAndPort)

    print "\033[;32;1mlocalIpAndPort :\033[0m", localIpAndPort
    print "\033[;32;1mtargetIpAndPort : \033[0m", targetIpAndPort

    me.bind(tuple(localIpAndPort))
    me.listen(USERNUMBER)

    you.connect(tuple(targetIpAndPort))

    shiehChatWindow = ShiehChatWindow(you, me)

    return (you, me)

def main():
    options = interfaceCL()

    if options[0].gui:
        you, me = startChatGUI()

        you.close()
        me.close()

    else:
        startChat()


if __name__ == '__main__':
    main()
