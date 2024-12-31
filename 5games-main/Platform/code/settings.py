import pygame
from os import walk
from os.path import join
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2
from random import randint, randrange, uniform

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
TILE_SIZE = 64 
FRAMERATE = 60
BG_COLOR = '#fcdfcd'
