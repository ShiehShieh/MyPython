#!/usr/bin/env python
# encoding: utf-8
##
# @file GreeceWarMain.py
# @brief A game on Greece war.
# @author 谢志杰/Zhijie Shieh
# @E-mail xie510894496@gmail.com
# @version 1.0v
# @date 2014-07-03


import os
import sys
import pygame
import Tkinter
from pygame.locals import *
from GameObject import *
from Utility import *

if not pygame.font  : print 'warning, can not load the font.'
if not pygame.mixer : print 'warning, can not load the mixer.'


VERSION = '1.0v'


class TimeHandler(pygame.sprite.Sprite):

    """Docstring for TimeHandler. """

    def __init__(self, screen, number, category):
        """@todo: to be defined1. """
        super(TimeHandler, self).__init__()
        self.myTime           = number
        self.category         = category
        self.screen           = screen
        self.image, self.rect = loadImage('Number%s.png' % (self.myTime))

        if isinstance(screen, pygame.Surface):
            self.rect.centerx = screen.get_rect().centerx / 5
            self.rect.centery = screen.get_rect().centery / 5
        elif isinstance(screen, pygame.sprite.Sprite):
            self.rect.centerx = screen.rect.centerx + screen.rect.width
            self.rect.centery = screen.rect.centery

    def update(self, position = None):
        """@todo: Docstring for update.
        :posi   : @Must be a tuple.
        :returns: @todo

        """
        maxMonth = (1, 3, 5, 7, 8, 10, 12,)
        zero_two = (0, 2,)
        minMonth = (4, 6, 9, 11,)

        if self.category == 'hourTwo':
            self.myTime = self.myTime + 1
            if self.screen.myTime != 2:
                if self.myTime == 10:
                    self.myTime = 0
                    self.screen.myTime = self.screen.myTime + 1
            elif self.screen.myTime == 2:
                if self.myTime == 4:
                    self.myTime = 0
                    self.screen.myTime = self.screen.myTime + 1

        elif self.category == 'hourOne':
            if self.myTime == 3:
                self.myTime = 0
                self.screen.myTime = self.screen.myTime + 1

        elif self.category == 'dayTwo':
            if self.screen.screen.screen.myTime == 0 and self.screen.screen.myTime in minMonth or \
                    self.screen.screen.screen.myTime == 1 and self.screen.screen.myTime == 1:
                if self.myTime == 10:
                    self.myTime = 0
                    self.screen.myTime = self.screen.myTime + 1
            elif self.screen.screen.screen.myTime == 0 and self.screen.screen.myTime in maxMonth or \
                    self.screen.screen.screen.myTime == 1 and self.screen.screen.mytime in zero_two:
                if self.screen.myTime != 3 and self.myTime == 10:
                    self.myTime = 0
                    self.screen.myTime = self.screen.myTime + 1
                elif self.screen.myTime == 3 and self.myTime == 2:
                    self.myTime = 0
                    self.screen.myTime = self.screen.myTime + 1

        elif self.category == 'dayOne':
            if self.screen.screen == 0 and self.screen == 2:
                if self.myTime == 3:
                    self.myTime = 0
                    self.screen.myTime = self.screen.myTime + 1
            elif self.myTime == 4:
                self.myTime = 0
                self.screen.myTime = self.screen.myTime + 1

        elif self.category == 'monthTwo':
            if self.screen.myTime == 0:
                if self.myTime == 10:
                    self.myTime = 0
                    self.screen.myTime = self.screen.myTime + 1
            elif self.screen.myTime == 1:
                if self.myTime == 3:
                    self.myTime = 0
                    self.screen.myTime = self.screen.myTime + 1

        elif self.category == 'monthOne':
            if self.myTime == 2:
                self.myTime = 0
                self.screen.myTime = self.screen.myTime + 1

        elif self.category == 'yearFour':
            if self.myTime == 10:
                self.myTime = 0
                self.screen.myTime = self.screen.myTime + 1

        elif self.category == 'yearThree':
            if self.myTime == 10:
                self.myTime = 0
                self.screen.myTime = self.screen.myTime + 1

        elif self.category == 'yearTwo':
            if self.myTime == 10:
                self.myTime = 0
                self.screen.myTime = self.screen.myTime + 1

        elif self.category == 'yearOne':
            if self.myTime == 10:
                self.myTime = 0
                raise TimeOut()

        self.image = loadImage('Number%s.png' % (self.myTime))[0]

        if position:
            self.rect.centerx, self.rect.centery = position

    def get_time(self):
        """@todo: Docstring for get_time.
        :returns: @todo

        """
        return pygame.time.get_ticks()


def main():
    """@todo: Docstring for main.
    :returns: @todo

    """
    #Initialize the screen.
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Greece War.')

    #Inititalize the background image.
    (backgroundCat, backgroundCatRect) = loadImage('LookIntoMyEyes.jpg')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((146, 146, 146))
    background.blit(backgroundCat, backgroundCatRect)

    #Initialize all the hero and soldier.
    hero         = Hero()
#   city         = City('City')
    heroGroup    = pygame.sprite.Group(hero)
    soldierGroup = pygame.sprite.Group()
#   cityGroup    = pygame.sprite.Group(city)
    heroGroup.draw(screen)
    soldierGroup.draw(screen)

    #Initial the TimeHandler.
    yearOne = TimeHandler(screen, 5, 'yearOne')
    yearOne.update((screen.get_rect().centerx / 5, screen.get_rect().centery / 5))

    yearTwo          = TimeHandler(yearOne, 3, 'yearTwo')
    yearThree        = TimeHandler(yearTwo, 5, 'yearThree')
    yearFour         = TimeHandler(yearThree, 0, 'yearFour')
    monthOne         = TimeHandler(yearFour, 0, 'monthOne')
    monthTwo         = TimeHandler(monthOne, 1, 'monthTwo')
    dayOne           = TimeHandler(monthTwo, 0, 'dayOne')
    dayTwo           = TimeHandler(dayOne, 5, 'dayTwo')
    hourOne          = TimeHandler(dayTwo, 0, 'hourOne')
    hourTwo          = TimeHandler(hourOne, 1, 'hourTwo')
    timeHandlerGroup = pygame.sprite.Group(\
            (yearOne, yearTwo, yearThree, \
            yearFour, monthOne, monthTwo, \
            dayOne, dayTwo, hourOne, hourTwo))
    timeHandlerGroup.draw(screen)

    #Blit all.
    screen.blit(background, (0, 0))
    pygame.display.flip()

    #load the background music.
    backgroundMusic = loadSound('MainTheme.wav')

    clock           = pygame.time.Clock()

    while True:
        clock.tick(1)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_h:
                    print 'pass'

                if event.key == K_m:
                    backgroundMusic.play()

                if event.key == K_s:
                    heavyInfantry = Soldier('HeavyInfantry')
                    soldierGroup.add(heavyInfantry)

                if event.key == K_a:
                    archer = Soldier('Archer')
                    soldierGroup.add(archer)

                if event.key == K_UP:
                    hero.update('up')

                if event.key == K_DOWN:
                    hero.update('down')

                if event.key == K_LEFT:
                    hero.update('left')

                if event.key == K_RIGHT:
                    hero.update('right')

        screen.blit(background, (0, 0))

        soldierGroup.update()
#       cityGroup.update(True, (0, 5, 0),  True, (0, 0), True, {})
        timeHandlerGroup.update()

        heroGroup.draw(screen)
        soldierGroup.draw(screen)
#       cityGroup.draw(screen)
        timeHandlerGroup.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()

