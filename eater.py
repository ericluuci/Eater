# Eric Lu

import pygame
from pygame import *
import sys
from random import randint

def start():
    
    # Creates window and title
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption('Eater - Eric Lu')
    
    # Loads background image
    bg = pygame.image.load('background.jpg')
    bg = pygame.transform.scale(bg, (1000, 600))
    screen.blit(bg, (0, 0))

    # Write Title
    font1 = pygame.font.SysFont('Times New Roman', 80)
    title_text = font1.render('EATER', 1, (0, 0, 0))
    screen.blit(title_text, (650, 35))

    # Write 'Eric Lu'
    font2 = pygame.font.SysFont('Times New Roman', 36)
    eric_text = font2.render('Eric Lu', 1, (0, 0, 0))
    screen.blit(eric_text, (720, 125))

    # Write 'Press Any Key To Begin'
    font3 = pygame.font.SysFont('Times New Roman', 30)
    press_text = font3.render('Press Any Key To Begin', 1, (0, 0, 0))
    screen.blit(press_text, (630, 490))

    # Draw Character
    char = pygame.image.load('character_eat.png')
    char = pygame.transform.scale(char, (500, 500))
    screen.blit(char, (50, 50))
    
    # Draw Block
    block = pygame.image.load('ice_block2.png')
    block = pygame.transform.scale(block, (250, 250))
    screen.blit(block, (650, 195))

    while True:
        
        for e in pygame.event.get():
            if (e.type == KEYDOWN):
                return
            
        pygame.display.update() 

def main():

    direction = 0
    points = 0
    right = False
    left = False
    up = False
    down = False
    counter = 40
    blockList = []
    gameOver = False

    # Create a sprite group
    entities = pygame.sprite.Group()

    # Adds player to the group
    player = Player(495, 295, 10)
    entities.add(player)
    
    # Creates window and title
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption('Eater - Eric Lu')

    # Loads background image
    bg = pygame.image.load('background.jpg')
    bg = pygame.transform.scale(bg, (1000, 600))

    # Loads ice block images
    block1 = pygame.image.load('ice_block1.png')
    block2 = pygame.image.load('ice_block2.png')
    block3 = pygame.image.load('ice_block3.png')
    block4 = pygame.image.load('ice_block4.png')
    
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for e in pygame.event.get():

            if (e.type == QUIT):
                pygame.quit()
                sys.exit()
                
                
            if (e.type == KEYDOWN and (e.key == K_RIGHT or e.key == K_d)):
                right = True
                direction = 0

            if (e.type == KEYDOWN and (e.key == K_LEFT or e.key == K_a)):
                left =  True
                direction = 180

            if (e.type == KEYDOWN and (e.key == K_UP or e.key == K_w)):
                up = True
                direction = 90

            if (e.type == KEYDOWN and (e.key == K_DOWN or e.key == K_s)):
                down = True
                direction = 270


            if (e.type == KEYUP and (e.key == K_RIGHT or e.key == K_d)):
                right = False

            if (e.type == KEYUP and (e.key == K_LEFT or e.key == K_a)):
                left = False

            if (e.type == KEYUP and (e.key == K_UP or e.key == K_w)):
                up = False

            if (e.type == KEYUP and (e.key == K_DOWN or e.key == K_s)):
                down = False

            # Waiting for the user to press 'R' after 'Game Over'
            if (gameOver == True and e.type == KEYDOWN and e.key == K_r):
                gameOver = False
                direction = 0
                points = 0
                right = False
                left = False
                up = False
                down = False
                counter = 40
                blockList = []
                gameOver = False
                entities = pygame.sprite.Group()
                player = Player(495, 295, 10)
                entities.add(player)

        if (gameOver == False):

            # Adds blocks every 40ms
            if (counter == 40):
                counter = 0
                block = Block()
                entities.add(block)
                blockList.append(block)

            counter += 1

            # Draw background    
            screen.blit(bg, (0, 0))

            # Draw points
            font = pygame.font.SysFont('Times New Roman', 24)
            points_text = font.render('Points : ' + str(points), 1, (0, 0, 0))
            screen.blit(points_text, (875, 10))

            # Update player and block
            temp = player.update(right, left, up, down, direction, blockList)
            if (type(temp) == int):
                points += temp
            else:
                gameOver = True
            for sprite in entities:
                if (str(sprite) == "<Block sprite(in 1 groups)>"):
                    sprite.update()

            # Draw sprites
            entities.draw(screen)

        elif (gameOver == True):

            # Write 'Game Over!'
            font1 = pygame.font.SysFont('Times New Roman', 72)
            end_text = font1.render('Game Over!', 1, (0, 0, 0))
            screen.blit(end_text, (350, 100))

            # Write 'Press 'R' to try again!'
            font2 = pygame.font.SysFont('Times New Roman', 54)
            retry_text = font2.render("Press 'R' to try again!", 1, (0, 0, 0))
            screen.blit(retry_text, (300, 400))

        # Update screen
        pygame.display.update()

class Entity(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):

    def __init__(self, x, y, side):
        
        Entity.__init__(self)
        self.image_base = pygame.image.load('character_eat.png')
        self.rect = Rect(x, y, side, side)

        self.rect.x = x
        self.rect.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.side = side

    def update(self, right, left, up, down, direction, blockList):

        # X Boundary
        if (self.rect.x < 0):
            self.rect.x = 0
            self.x_vel = 0
        elif (self.rect.x + self.side >= 1000):
            self.rect.x = 1000 - self.side
            self.x_vel = 0

        # Y Boundary
        if (self.rect.y  < 0):
            self.rect.y = 0
            self.y_vel = 0
        elif (self.rect.y + self.side >= 600):
            self.rect.y = 600 - self.side
            self.y_vel = 0
        
        # Increases the character's velocity
        if (right):
            self.x_vel += 0.15
        if (left):
            self.x_vel -= 0.15
        if (up):
            self.y_vel -= 0.15
        if (down):
            self.y_vel += 0.15

        # Simulates x-axis friction
        if (self.x_vel >= -0.05 and self.x_vel <= 0.05):
            self.x_vel = 0
        elif (self.x_vel > 0):
            self.x_vel -= 0.05
        elif (self.x_vel < 0):
            self.x_vel += 0.05

        # Simulates y-axis friction
        if (self.y_vel >= -0.05 and self.y_vel <= 0.05):
            self.y_vel = 0
        elif (self.y_vel > 0):
            self.y_vel -= 0.05
        elif (self.y_vel < 0):
            self.y_vel += 0.05

        # Adds the position according to velocity
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        self.rect = Rect(self.rect.x, self.rect.y, self.side, self.side)

        #Scales and rotates the character image
        self.image = pygame.transform.scale(self.image_base, (self.side, self.side))
        self.image = pygame.transform.rotate(self.image, direction)

        return (self.collide(blockList))
        

    def collide(self, blockList):

        points = 0
        for hit in blockList:
            if pygame.sprite.collide_rect(self, hit):

                if (self.side >= hit.side):
                    # Player eats block
                    self.side += 1
                    points += hit.side
                    hit.rect.x = -999
                    hit.rect.y = -999
                    
                else:
                    # Game Over
                    return

        return points
        
class Block(Entity):

    def __init__(self):

        Entity.__init__(self)

        self.movement = randint(1, 4) # Determines movement
        self.side = randint(2, 60) # Length of the block
        
        if (self.movement % 2 == 0): # Moves Horizontally
            self.y = randint(0, 600)
            
            if (self.movement == 2): # Left to Right
                self.x = -self.side
                self.vel = randint(1, 3)
                
            elif (self.movement == 4): # Right to Left
                self.x = 1000
                self.vel = -randint(1,3)

        elif (self.movement % 2 == 1): # Moves Vertically
            self.x = randint(0, 1000)
            
            if (self.movement == 1): # Top to Bottom
                self.y = -self.side
                self.vel = randint(1, 3)
                
            elif (self.movement == 3): # Bottom to Top
                self.y = 600
                self.vel = -randint(1,3)
                
        self.pic = randint(1, 4) # Determines 1-4 image
        self.image = pygame.image.load('ice_block'+str(self.pic)+'.png')
        self.image = pygame.transform.scale(self.image, (self.side, self.side))
        self.rect = Rect(self.x, self.y, self.side, self.side)

        self.rect.x = self.x
        self.rect.y = self.y
            
    def update(self):

        # Moves block at constant velocity
        if (self.movement % 2 == 0):
            self.rect.x += self.vel
        elif (self.movement % 2 == 1):
            self.rect.y += self.vel

        self.image = pygame.transform.scale(self.image, (self.side, self.side))
        self.rect = Rect(self.rect.x, self.rect.y, self.side, self.side)

if __name__ == '__main__':
    start()
    main()
