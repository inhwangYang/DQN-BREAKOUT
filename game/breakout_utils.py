import pygame
import sys
import os

def load():
    # path of player with different states
    IMAGES= {}

    # sounds
    soundExt = '.wav'
    #SOUNDS['blip']    = pygame.mixer.Sound('blip' + soundExt)
    
    print(os.getcwd())

    # select random player sprites
    IMAGES['bat'] = (
        pygame.image.load(os.getcwd()+'/game/bat.png').convert_alpha(),
    )
    IMAGES['ball'] = (
        pygame.image.load(os.getcwd()+'/game/ball.png').convert_alpha(),
    )
    IMAGES['brick'] = (
        pygame.image.load(os.getcwd()+'/game/brick.png').convert_alpha(),
    )

    return IMAGES

