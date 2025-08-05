import pygame, sys
from pygame.locals import*


class Units:
    def __init__(self, id:int, image_path:str, health:int, damage:int, attackRate:int, speed:int, range:int, side:bool):
        self.id = id
        self.image = pygame.transform.scale(
            pygame.image.load(image_path), (120, 180)  # <-- set your desired width and height here
        )
        self.dead = False
        self.health = health
        self.damage = damage
        self.speed = speed
        self.range = range
        self.position = 100*side
        self.side = side
        # self.card = Card  # Removed or replace with actual Card instance if needed
    def update(self):
        pass

    def attack(self):
        pass

    def move(self):
        # change position
        if self.side and self.position >= 0:
            self.position -= self.speed
        elif self.position <= 100:
            self.position += self.speed
    def takeDamage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.dead = True
    def attack(self, target):
        self.aCounter += 1
        if self.aCounter % self.attackRate == 0:
            target.takeDamage(self.damage)
    def update(self):
        # find enemies
        enemies = main.enemies
        if self.side:
            enemies = main.allies
        for enemy in enemies: # enemies is placeholder, list of enemy units
            if abs(enemy.position - self.position) < self.range:
                self.attack(self, enemy)
            else:
                self.move(self)
