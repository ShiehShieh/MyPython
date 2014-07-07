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
from pygame.locals import *
from GameObject import *
from Utility import *

if not pygame.font  : print 'warning, can not load the font.'
if not pygame.mixer : print 'warning, can not load the mixer.'


VERSION = '1.0v'


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
    city         = City('City')
    heroGroup    = pygame.sprite.Group(hero)
    soldierGroup = pygame.sprite.Group()
    cityGroup    = pygame.sprite.Group(city)
    heroGroup.draw(screen)
    soldierGroup.draw(screen)

    #Blit all.
    screen.blit(background, (0, 0))
    pygame.display.flip()

    #load the background music.
    backgroundMusic = loadSound('MainTheme.wav')

    clock           = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_h:
                    print 'pass'

                if event.key == K_m:
                    backgroundMusic.play()
                    print 'Music begin.'

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
        cityGroup.update(True, (0, 0, 10),  True, (0, 0), True, {})
        heroGroup.draw(screen)
        soldierGroup.draw(screen)
        cityGroup.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()

