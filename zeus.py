#!/usr/bin/env python

import sys
import os
import urllib


def urlTest():
    """@todo: Docstring for urlTest.

    :returns: @todo

    """
    urlopenerTest = urllib.urlopen("http://www.baidu.com")
    with open("urlTest.txt", "w") as urlOutput:
        rawData = urlopenerTest.read()
        content = ">\n".join(rawData.split(">"))
        urlOutput.write(content)


def main():
    print os.path.dirname(__file__)
    print 'Python.'
    print sys.path
    urlTest();


if __name__ == '__main__':
    main()

