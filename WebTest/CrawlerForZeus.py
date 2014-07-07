#!/usr/bin/env python
# encoding: utf-8


"""A crawler utility"""
##
# @file CrawlerForZeus.py
# @brief 
# @author 谢志杰
# @version 1.0
# @date 2014-06-27


import os
import sys
import time
import urllib
import htmllib
import os.path
import urlparse
import optparse
import formatter
import cStringIO


USAGE   = '%s [option] arg1 arg2' % (sys.argv[0])
VERSION = 'v1.0'


class CertainPage(object):

    """Docstring for CertainPage. """

    def __init__(self, url):
        """@todo: to be defined1. """
        self.url = url
        self.urlFile = self.fileSystem(url)

    def download(self):
        """@todo: Docstring for download.
        :returns: @todo

        """
        try:
            localFile = urllib.urlretrieve(self.url, self.urlFile)

            print "\033[0;34;1mURL %s have been download just now.\033[0m" % (self.url)
        except Exception:
            localFile = "$$$ Error : invaild URL : %s" % (self.url)

        return localFile

    def fileSystem(self, url, defaultName = "index.html"):
        """@todo: Docstring for fileSystem.

        :url: @todo
        :defaultName: @todo
        :returns: @todo

        """
        urlStructure = urlparse.urlparse(url)
        path         = urlStructure[1] + urlStructure[2]
        dirTree      = os.path.splitext(path)

        if len(urlStructure[2]) == 0 or urlStructure[2] == '/':
            if path[-1] == '/':
                path += defaultName
            else:
                path += '/' + defaultName
        else:
            if os.sep != '/':
                path.replace('/', os.sep)

        ldir = os.path.dirname(path)
        dirTuple = ['/'.join(ldir.split('/')[ : i + 1]) for i in range(len(ldir.split('/')))]
        if not os.path.isdir(ldir):
            for subDir in dirTuple:
                if os.path.exists(unicode(subDir)):
                    continue
                os.mkdir(unicode(subDir))

        return path

    def parserHTML(self):
        """@todo: Docstring for findLinks.
        :returns: @todo

        """
        self.htmlParser = htmllib.HTMLParser(formatter.AbstractFormatter(formatter.DumbWriter(cStringIO.StringIO())))
        self.htmlParser.feed(open(self.urlFile).read())
        self.htmlParser.close()

        return self.htmlParser.anchorlist


class Manager(object):

    """Docstring for Manager. """

    def __init__(self, url):
        """@todo: to be defined1.

        :url: @todo

        """
        self.url      = url
        self.todoList = [self.url]
        self.done     = []
        self.domain   = urlparse.urlparse(self.url)[1]

    def getAllAnchors(self, url):
        """@todo: Docstring for getAllAnchor.

        :returns: @todo

        """
        mainPage = CertainPage(url)

        mainPage.download()

        if url[0] == '$':
            print url
            
            return 1

        self.done.append(url)

        anchorInHtml = mainPage.parserHTML()

        for link in anchorInHtml:
            if link[0] == '/':
                link = urlparse.urljoin(url, link)
            if link.find(self.domain) != -1:
                if link not in self.todoList:
                    if link not in self.done:
                        self.todoList.insert(0, link)
                        print "\033[0;32;1mURL %s is added.\033[0m" % (link)
                    else:
                        print "\033[0;37;1mURL %s have been download before.\033[0m" % (link)
                else:
                    print "\033[0;33;1mURL %s has already been added into the to-do list.\033[0m" % (link)
            else:
                print "\033[0;31;1mURL %s have't the same domain name with main page.\033[0m" % (link)

        time.sleep(5)
        return 0

    def getAllPages(self):
        """@todo: Docstring for getAllPages.

        :returns: @todo

        """
        while self.todoList:
            suburl = self.todoList.pop()

            self.getAllAnchors(suburl)


def interfaceCL():
    """@todo: Docstring for interfaceCL.
    :returns: @todo

    """
    myParser = optparse.OptionParser(usage = USAGE, version = VERSION)

    myParser.add_option('-v', '--verbose', action = 'store_true', dest  = 'verbose', help = 'Output verbosely')
    myParser.add_option('-q', '--quiet', action   = 'store_false', dest = 'verbose', help = 'Output quietly')

    options = myParser.parse_args()

    return options


def main():
    options = interfaceCL()

    if len(sys.argv) > 1 and sys.argv[-1].find('http') != -1:
        manager = Manager(sys.argv[-1])
    else:
        manager = Manager(raw_input("URL :"))

    manager.getAllPages()

if __name__ == '__main__':
    main()

