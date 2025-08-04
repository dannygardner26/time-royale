import pygame, sys
from pygame.locals import*
import Card

class Units:
    def __init__(self, card:Card, side:bool):
        self.position = 100*side
        self.side = side
        self.card = card
    def update(self):
        
    def attack(self):

    def move(self):
        # check to see enemy or tower
        # change position
        if self.side and self.position >= 0:
            self.position -= self.card.speed
        elif self.position <= 100:
            self.position += self.card.speed
        
