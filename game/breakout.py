#!/usr/bin/env python

#
#   Breakout V 0.1 June 2009
#
#   Copyright (C) 2009 John Cheetham    
#
#   web   : http://www.johncheetham.com/projects/breakout
#   email : developer@johncheetham.com
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#    
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys, pygame, random
import pygame.surfarray as surfarray
from pygame.locals import *
from itertools import cycle
from game import breakout_utils
import os

FPS = 30

FPSCLOCK = pygame.time.Clock()

pygame.init()   

size = width, height = 640, 480
screen = pygame.display.set_mode(size)
#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

IMAGES = breakout_utils.load()

class Breakout():
   
    def __init__(self):
        self.xspeed_init = 6
        self.yspeed_init = 6
        self.max_lives = 5
        self.bat_speed = 30
        self.score = 0 
        self.bgcolour = 0x2F, 0x4F, 0x4F  # darkslategrey     
   
        self.bat = pygame.image.load(os.getcwd() + "/game/bat.png").convert()
        self.batrect = self.bat.get_rect()

        self.ball = pygame.image.load(os.getcwd() + "/game/ball.png").convert()
        self.ball.set_colorkey((255, 255, 255))
        self.ballrect = self.ball.get_rect()
       
        #pong = SOUNDS['blip']
        #pong.set_volume(10)        
        
        self.wall = Wall()
        self.wall.build_wall(width)

        # Initialise ready for game loop
        self.batrect = self.batrect.move((width / 2) - (self.batrect.right / 2), height - 20)
        self.ballrect = self.ballrect.move(width / 2, height / 2)       
        self.xspeed = self.xspeed_init
        self.yspeed = self.yspeed_init
        self.lives = self.max_lives
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(1,30)       
        pygame.mouse.set_visible(0)       # turn off mouse pointer
   
   
    def frame_step(self,input_actions):
          
        while 1:

            # 60 frames per second
            self.clock.tick(60)

            terminal = False
            
            if sum(input_actions) != 1:
                raise ValueError('Multiple input actions!')
            
            # process key presses
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
        	            sys.exit()
                    #if event.key == pygame.K_LEFT:                        
            if input_actions[0] == 1 :
                print("left")
                self.batrect = self.batrect.move(-self.bat_speed, 0)     
                if (self.batrect.left < 0):                           
                    self.batrect.left = 0      
                    #if event.key == pygame.K_RIGHT:                    
            if input_actions[1] == 1 :
                print("right")
                self.batrect = self.batrect.move(self.bat_speed, 0)
                if (self.batrect.right > width):                            
                    self.batrect.right = width

            # check if bat has hit ball    
            if self.ballrect.bottom >= self.batrect.top and \
               self.ballrect.bottom <= self.batrect.bottom and \
               self.ballrect.right >= self.batrect.left and \
               self.ballrect.left <= self.batrect.right:
                self.yspeed = -self.yspeed                
                #self.pong.play(0)                
                self.offset = self.ballrect.center[0] - self.batrect.center[0]                          
                # offset > 0 means ball has hit RHS of bat                   
                # vary angle of ball depending on where ball hits bat                      
                if self.offset > 0:
                    if self.offset > 30:  
                        self.xspeed = 7
                    elif self.offset > 23:                 
                        self.xspeed = 6
                    elif self.offset > 17:
                        self.xspeed = 5 
                else:  
                    if self.offset < -30:                             
                        self.xspeed = -7
                    elif self.offset < -23:
                        self.xspeed = -6
                    elif self.xspeed < -17:
                        self.xspeed = -5     
                      
            # move bat/ball
            self.ballrect = self.ballrect.move(self.xspeed, self.yspeed)
            if self.ballrect.left < 0 or self.ballrect.right > width:
                self.xspeed = -self.xspeed                
               # self.pong.play(0)            
            if self.ballrect.top < 0:
                self.yspeed = -self.yspeed                
                #self.pong.play(0)               

            # check if ball has gone past bat - lose a life
            if self.ballrect.top > height:
                self.lives -= 1
                # start a new ball
                xspeed = self.xspeed_init
                rand = random.random()                
                if random.random() > 0.5:
                    self.xspeed = -self.xspeed 
                self.yspeed = self.yspeed_init            
                self.ballrect.center = width * random.random(), height / 3                                
                if self.lives == 0:   
                    terminal = True                 
                    msg = pygame.font.Font(None,70).render("Game Over", True, (0,255,255), self.bgcolour)
                    msgrect = msg.get_rect()
                    msgrect = msgrect.move(width / 2 - (msgrect.center[0]), height / 3)
                    screen.blit(msg, msgrect)
                    pygame.display.flip()
                    # process key presses
                    #     - ESC to quit
                    #     - any other key to restart game
                    while 1:
                        restart = True
                          
                            
                          #  for event in pygame.event.get():
                         #       if event.type == pygame.QUIT:
                          #          sys.exit()
                           #     if event.type == pygame.KEYDOWN:
                            #    if event.key == pygame.K_ESCAPE:
                             #       sys.exit()
                              #  if not (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):                                    
                               #     restart = True 
                          
                          
                        if restart:                   
                            screen.fill(self.bgcolour)
                            self.wall.build_wall(width)
                            self.lives = self.max_lives
                            self.score = 0
                            break
            
            if self.xspeed < 0 and self.ballrect.left < 0:
                self.xspeed = -self.xspeed                                
                #self.pong.play(0)

            if self.xspeed > 0 and self.ballrect.right > width:
                self.xspeed = -self.xspeed                               
                #self.pong.play(0)
           
            # check if ball has hit wall
            # if yes yhen delete brick and change ball direction
            index = self.ballrect.collidelist(self.wall.brickrect)       
            if index != -1: 
                if self.ballrect.center[0] > self.wall.brickrect[index].right or \
                   self.ballrect.center[0] < self.wall.brickrect[index].left:
                    self.xspeed = -self.xspeed
                else:
                    self.yspeed = -self.yspeed                
                #self.pong.play(0)              
                self.wall.brickrect[index:index + 1] = []
                self.score += 10
                          
            screen.fill(self.bgcolour)
            scoretext = pygame.font.Font(None,40).render(str(self.score), True, (0,255,255), self.bgcolour)
            scoretextrect = scoretext.get_rect()
            scoretextrect = scoretextrect.move(width - scoretextrect.right, 0)
            screen.blit(scoretext, scoretextrect)

            for i in range(0, len(self.wall.brickrect)):
                screen.blit(self.wall.brick, self.wall.brickrect[i])    

            # if wall completely gone then rebuild it
            if self.wall.brickrect == []:              
                self.wall.build_wall(width)                
                self.xspeed = self.xspeed_init
                self.yspeed = self.yspeed_init                
                self.ballrect.center = width / 2, height / 3
         
            screen.blit(self.ball, self.ballrect)
            screen.blit(self.bat, self.batrect)
            pygame.display.flip()
            
            image_data = pygame.surfarray.array3d(pygame.display.get_surface())
            pygame.display.update()
            FPSCLOCK.tick(FPS)
            
            return image_data,self.score, terminal
            

class Wall():

    def __init__(self):
        self.brick = pygame.image.load(os.getcwd() + "/game/brick.png").convert()
        brickrect = self.brick.get_rect()
        self.bricklength = brickrect.right - brickrect.left       
        self.brickheight = brickrect.bottom - brickrect.top             

    def build_wall(self, width):        
        xpos = 0
        ypos = 60
        adj = 0
        self.brickrect = []
        for i in range (0, 52):           
            if xpos > width:
                if adj == 0:
                    adj = self.bricklength / 2
                else:
                    adj = 0
                xpos = -adj
                ypos += self.brickheight
                
            self.brickrect.append(self.brick.get_rect())    
            self.brickrect[i] = self.brickrect[i].move(xpos, ypos)
            xpos = xpos + self.bricklength

if __name__ == '__main__':
    br = Breakout()
    br.main()


