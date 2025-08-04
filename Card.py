import pygame, sys
from pygame.locals import*

class Card:
    def __init__(self, id:int, image_path:str, health:int, damage:int, speed:int, range:int):
        self.id = id
        self.image = pygame.image.load(image_path)
        self.health = health
        self.damage = damage
        self.speed = speed
        self.range = range

card = Card(1, 100, 10, 10, 20)
print(card.id)