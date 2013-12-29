#!/usr/bin/python
"""
|\ --- \  /  --- |
|/  |   \/  |    |
|   |   /\  |--  |
|  _|_ /  \ |___ |__
WRANGLER
"""
#Made by Kelton and his Dad
#v. 1 completed 12/27/13
import sys
import os
import pygame
import random

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
OBSTACLE_COUNT = 50
WIDTH = 640
HEIGHT = 400
RED = (255, 0, 0 )
WHITE = (255, 255, 255)

class MovingPixel:


    def __init__(self, surface, x, y):
        """Creates a Moving Pixel"""
        self.x = x
        self.y = y
        self.hdir = 0
        self.vdir = -1
        self.surface = surface
        self.crashed = False

    def direction(self, dir):
        """Changes the pixel's direction"""
        self.hdir, self.vdir = dir

    def move(self):
        """Moves the Pixel"""
        self.x += self.hdir
        self.y += self.vdir

        if self.x <= 0 or self.x >= WIDTH or self.y <= 0 or self.y >= HEIGHT:
            self.crashed = True
            return
        r, g, b, a = self.surface.get_at((self.x, self.y))
        if (r, g, b) != (0, 0, 0):
            self.crashed = True

    def draw(self, surface):
        surface.set_at((self.x, self.y), WHITE)



def create_obstacles(count):
    pix_collection = []
    for i in range(0,count):
        create_obstacle(pix_collection)
    return pix_collection

def create_obstacle(collection):
    random_pixel = (random.randint(1, WIDTH-1), random.randint(1, HEIGHT-1))
    collection.append( (random_pixel[0]-1, random_pixel[1]) )
    collection.append( (random_pixel[0]+1, random_pixel[1]) )
    collection.append( (random_pixel[0], random_pixel[1]-1) )
    collection.append( (random_pixel[0], random_pixel[1]+1) )
    return

def get_highscore():
    highscore = -1
    
    if os.path.exists("highscore.txt") == False:
        # create the new file and set the score to 0
        file_handle = open("highscore.txt", 'w')
        file_handle.write( "0" )
        file_handle.close()
        highscore = 0
    else:
        # read in the highscore and return it
        file_handle = open("highscore.txt", 'r')
        highscore = int(file_handle.readline())
        file_handle.close()
        
    return highscore

def set_highscore(new_highscore):
    file_handle = open("highscore.txt", 'w')
    file_handle.write(str(new_highscore))
    file_handle.close()

# initialize the game

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Wrangler")
clock = pygame.time.Clock()
running = True
tick_count = 0
pygame.init()
# sound!
pygame.mixer.init()
pygame.mixer.music.load('retro.wav')
pygame.mixer.music.play(-1)

pix = MovingPixel(screen, WIDTH/2, HEIGHT/2)

random_pixels = create_obstacles(OBSTACLE_COUNT)
    
while running:
    RAND_DIR = random.randint(1, 4)
    pix.move()
    if pix.x <= 0 or pix.x >= WIDTH or pix.y <= 0 or pix.y >= HEIGHT or pix.crashed:
        print "Crash!"
        score = pygame.time.get_ticks() / 100
        if score > get_highscore():
            set_highscore(score)
            print "New Highscore!"
            
        print "Score:" + str(score)
        running = False
    
    screen.fill((0, 0, 0))

    # insert a new random_pixel every 200 ticks
    if tick_count == 200:
        create_obstacle(random_pixels)
        tick_count = 0
    else:
        tick_count += 10
        
    for pixel in random_pixels:
        screen.set_at(pixel, RED)
        
    pix.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            score = pygame.time.get_ticks() / 100
            if score > get_highscore():
                set_highscore(score)
                print "New Highscore!"
            
            print "Score:" + str(score)
            running = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pix.direction(UP)
            elif event.key == pygame.K_DOWN:
                pix.direction(DOWN)
            elif event.key == pygame.K_LEFT:
                pix.direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                pix.direction(RIGHT)

        if RAND_DIR == 1:
            pix.direction(RIGHT)
        elif RAND_DIR == 2:
            pix.direction(DOWN)
        elif RAND_DIR == 3:
            pix.direction(UP)
        elif RAND_DIR == 4:
            pix.direction(LEFT)

    pygame.display.flip()
    clock.tick(100)
