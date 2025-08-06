import pygame
from pygame.locals import*

class Spells:
    def __init__(self, image_path:str, damage:int, radius:int, location:int):
        self.img = pygame.image.load(image_path).convert_alpha()
        self.damage = damage
        self.radius = radius
        self.location = location
    def dealDamage(self, enemies):
        for enemy in enemies:
            if not enemy.dead:
                    if abs(self.location - enemy.position) <= self.radius:
                        enemy.takeDamage(self.damage)
    def cast(self, enemies):
        self.dealDamage(enemies)