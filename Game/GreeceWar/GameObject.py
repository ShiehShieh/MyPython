#!/usr/bin/env python
# encoding: utf-8
##
# @file GreeceWarMain.py
# @brief A game on Greece war.
# @author 谢志杰/Zhijie Shieh
# @E-mail xie510894496@gmail.com
# @version 1.0v
# @date 2014-07-04


import pygame
from pygame.locals import *
from Utility import *


VERSION = '1.0v'


class Hero(pygame.sprite.Sprite):

    """Docstring for Hero. """

    def __init__(self):
        """@todo: to be defined1. """
        pygame.sprite.Sprite.__init__(self)

        (self.image, self.rect) = loadImage('Hero.jpeg')
        self.rect.center        = pygame.display.get_surface().get_rect().center
        self.coordinate         = self.rect.centerx, self.rect.centery

    def update(self, destination):
        """@todo: Docstring for update.

        :destination: @todo
        :returns: @todo

        """
        self.moveTo(destination)

    def moveTo(self, destination):
        """@todo: Docstring for moveTo.

        :destination: @todo
        :returns: @todo

        """
        if destination == 'up' :
            self.rect.centery = self.rect.centery - 10
        elif destination == 'down' :
            self.rect.centery = self.rect.centery + 10
        elif destination == 'left':
            self.rect.centerx = self.rect.centerx - 10
        else:
            self.rect.centerx = self.rect.centerx + 10


class Soldier(pygame.sprite.Sprite):

    """Docstring for Soldier. """

    def __init__(self, branch):
        """@todo: to be defined1. """
        pygame.sprite.Sprite.__init__(self)

        self.branch               = branch
        if  self.branch  == 'HeavyInfantry':
            self.image, self.rect = loadImage('HeavyInfantry.png')
        elif self.branch == 'Archer':
            self.image, self.rect = loadImage('Archer.png')
        elif self.branch == 'Knight':
            self.image, self.rect = loadImage('Knight.png')
        elif self.branch == 'Mariner':
            self.image, self.rect = loadImage('Mariner.png')
        else:
            pass

    def update(self):
        """@todo: Docstring for update.
        :returns: @todo

        """
        if self.branch == 'HeavyInfantry':
            self.rect.centerx = self.rect.centerx + 10
        elif self.branch == 'Archer':
            self.rect.centerx = self.rect.centerx + 10
        else:
            pass


class City(pygame.sprite.Sprite):

    """Docstring for City. """

    def __init__(self, cityName, treasure = ['normal', 0, 100, 0,],  population = [10000, 2000], troop = {'heavyInfantry' : 200}, hero = None):
        """@todo: to be defined1.

        :cityName: @The name of the city-state or city.
        :treasure: @(vpoor/poor/normal/rich/vrich, g, s, b)
        :popul   : @(total, citizen)
        :troop   : @{heavyInfantry:value, archer:value,
                    knight:value, mariner:value, ship:value)

        """
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = loadImage(cityName + '.jpg')
        self.cityName         = cityName
        self.treasure         = treasure
        self.population       = population
        self.troop            = troop
        self.hero             = hero

    def update(self, RAE = False, RAEarg = (0, 0, 0),  IP = False, IParg = (0, 0), TA = False, TAarg = {}):
        """@todo: Docstring for update.
        :returns: @todo

        """
        if RAE:
            self.revenueAndExpense(RAEarg)

            #upgrade the self.treasure[1 : 4] before upgrade self.treasure[0]
            self.upgradeMoney()

            if self.treasure[1] < 1:
                self.treasure[0] == 'vpoor'
            elif self.treasure[1] < 2:
                self.treasure[0] == 'poor'
            elif self.treasure[1] < 3:
                self.treasure[0] == 'normal'
            elif self.treasure[1] < 4:
                self.treasure[0] == 'rich'
            elif self.treasure[1] < 5:
                self.treasure[0] == 'vrich'

        elif IP:
            self.increasePeople(IParg)

        elif TA:
            self.trainArmy(TAarg)

    def upgradeMoney(self):
        """@todo: Docstring for upgradeMoney.
        :returns: @todo

        """
        #This variable is used to reresent the carry from the lower size.
        carry = 0

        if self.treasure[3] >= 100:
            carry = self.treasure[3] // 100
            self.treasure[3] = self.treasure[3] % 100
        if  carry != 0:
            self.treasure[2] = self.treasure[2] + carry
        if self.treasure[2] >= 100:
            carry = self.treasure[2] // 100
            self.treasure[2] = self.treasure[2] % 100
            self.treasure[1] = self.treasure[1] + carry

    def revenueAndExpense(self,  value):
        """@todo: Docstring for revenueAndExpense.

        :value: @The tuple of revenue and expense, can be minus.
        :returns: @todo

        """
        self.treasure = [self.treasure[0]] + [self.treasure[i + 1] + value[i] for i in range(3)]
        print self.treasure

    def increasePeople(self, value):
        """@todo: Docstring for increasePeople.

        :value: @The amount of population increasing.
        :returns: @todo

        """
        self.population = [self.population[i] + value[i] for i in range(2)]
        print self.population

    def trainArmy(self, **value):
        """@todo: Docstring for trainArmy.

        :value: @The resource you put into training.
        :returns: @todo

        """
        for branch in value.keys():
            self.troop[branch] = self.troop[branch] + value[branch]

        print self.troop

