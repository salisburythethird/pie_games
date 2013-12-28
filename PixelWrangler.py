"""
|\ --- \  /  --- |
|/  |   \/  |    |
|   |   /\  |--  |
|  _|_ /  \ |___ |__
WRANGLER
"""
#Made by Kelton and his Dad
#v. 1 completed 12/27/13

import pygame
import random

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
OBSTACLE_COUNT = 50
width = 640
height = 400
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

        if self.x <= 0 or self.x >= width or self.y <= 0 or self.y >= height:
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
        """random_pixel = (random.randint(1, width-1), random.randint(1, height-1))
        pix_collection.append( (random_pixel[0]-1, random_pixel[1]) )
        pix_collection.append( (random_pixel[0]+1, random_pixel[1]) )
        pix_collection.append( (random_pixel[0], random_pixel[1]-1) )
        pix_collection.append( (random_pixel[0], random_pixel[1]+1) )"""
        create_obstacle(pix_collection)
    return pix_collection

def create_obstacle(collection):
    random_pixel = (random.randint(1, width-1), random.randint(1, height-1))
    collection.append( (random_pixel[0]-1, random_pixel[1]) )
    collection.append( (random_pixel[0]+1, random_pixel[1]) )
    collection.append( (random_pixel[0], random_pixel[1]-1) )
    collection.append( (random_pixel[0], random_pixel[1]+1) )
    return

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pixel Wrangler")
clock = pygame.time.Clock()
running = True
tick_count = 0
pygame.init()

pix = MovingPixel(screen, width/2, height/2)

random_pixels = create_obstacles(OBSTACLE_COUNT)
    
while running:
    RAND_DIR = random.randint(1, 4)
    pix.move()
    if pix.x <= 0 or pix.x >= width or pix.y <= 0 or pix.y >= height or pix.crashed:
        print "Crash!"
        print "Score:" + str(pygame.time.get_ticks() / 100)
        running = False 
    
    screen.fill((0, 0, 0))

    # insert a new random_pixel every 200 ticks
    if tick_count == 200:
        create_obstacle(random_pixels)
        tick_count = 0
    else:
        tick_count += 10
        
    for pixel in random_pixels:
        screen.set_at(pixel, RED )
        
    pix.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print "Score:" + str(pygame.time.get_ticks() / 100)
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
