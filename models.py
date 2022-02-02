import pygame
from pygame import mixer
import random

# player class
class Player(object):

    def __init__(self):
        # Location
        self.x = 0
        self.y = 880

        self.color = (255, 0, 0) # red

        # hitbox
        self.hitbox = pygame.Rect(self.x, self.y, 25, 15)

        # health
        self.health = 20

    def get_keys(self):
        keys = pygame.key.get_pressed()
        dist = 5

        if keys[pygame.K_a]:
            # check to make sure its in the edge
            if self.x > dist:
                self.x -= dist

        elif keys[pygame.K_d]:
            if self.x < 700 - dist - 30:
                self.x += dist

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, 30, 20))

    def get_pos(self):
        return (self.x, self.y)

    def set_hitbox(self):
        self.hitbox = pygame.Rect(self.x, self.y, 25, 15)

    def damage(self, amount:int):
        self.health -= amount

    def get_health(self):
        return self.health

# bullet class
class Bullet(object):

    def __init__(self, start: tuple):
        self.x, self.y = start

        # velocity
        self.vel = 15

        # color
        self.color = (100, 100, 49)

        self.hitbox = pygame.Rect(self.x, self.y, 22, 22)

        # health system
        self.damage = 1

    def move(self):
        self.y -= self.vel

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, 15, 30))

    def get_damage(self):
        return self.damage

    def set_hitbox(self):
        self.hitbox = pygame.Rect(self.x, self.y, 22, 22)

class Enemy(object):

    def __init__(self, x:int, y:int):
        """
        creates an enemy at the top of the screen at x
        """
        self.x = x
        self.y = y

        self.color = (100, 240, 100)

        # 
        self.hitbox = pygame.Rect(self.x, self.y, 42, 42)

        self.damage = 1

        # add image
        n = random.randint(1, 9)
        self.image = pygame.image.load(f'bird{n}.png')
        self.image = pygame.transform.scale(self.image, (40, 40))


    def move(self):
        self.y += 2

    def draw(self, surface):
        # draw a sprite instead of the rectangle

        rect = self.image.get_rect()
        rect.center = self.x + 10, self.y + 10
        surface.blit(self.image, rect)
    
    def set_hitbox(self):
        self.hitbox = pygame.Rect(self.x, self.y, 22, 22)

    def get_damage(self):
        return self.damage

    def get_pos(self):
        return (self.x, self.y)

class HealthBar:

    def __init__(self):
        # set the locatation to the the upper left
        self.color = (255, 0, 0) # red

        self.x, self.y = (50, 50)

        # set value of health
        self.health = 100

    def remove(self):
        self.health -= 5

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.x + self.health, 25))

class GameOver:

    def __init__(self, screen):
        # self.screen = pygame.display.set_mode((700, 940))

        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("Game Over!", True, (255, 0, 0), (255, 0, 0))
        textRect = text.get_rect()
        textRect.center = (350, 490)
        screen.blit(text, textRect)