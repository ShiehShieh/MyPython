#!/usr/bin/env python
# encoding: utf-8
##
# @file GreeceWarMain.py
# @brief A game on Greece war.
# @author 谢志杰/Zhijie Shieh
# @E-mail xie510894496@gmail.com
# @version 1.0v
# @date 2014-07-04


import os
import sys
import pygame
from pygame.locals import *
from GameObject import *
from Utility import *


VERSION = '1.0v'


def loadImage(fileName):
    """@todo: Load the Image for game object.

    :fileName: @name of the image file.
    :returns: @A Image object if it exist.

    """
    try:
        filePath = os.path.join('Image', fileName)
        image    = pygame.image.load(filePath)
    except pygame.error, err:
        print 'Can not load the image file properly.'
        print err

        sys.exit(1)

    image = image.convert()
    image.set_colorkey(image.get_at((0, 0)))

    return image, image.get_rect()


def loadSound(fileName):
    """@todo: Load the Sound for game object.

    :fileName: @name of the sound file.
    :returns: @A Sound object if it exist.

    """
    class NoneSound(object):
        """Will be returned if can not load the sound."""
        def play(self):
            """@todo: Pretent to be a Sound object.
            """
            pass

    if not pygame.mixer:
        return NoneSound()

    try:
        filePath = os.path.join('Sound', fileName)
        sound    = pygame.mixer.Sound(filePath)

    except pygame.error, err:
        print 'Can not load the sound file properly.'
        print err

        return NoneSound()

    return sound

