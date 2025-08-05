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
        self.attackRate = attackRate
        self.aCounter = 0
        self.curTarget = None
    def move(self):
        # change position
        if self.side and self.position >= 0:
            self.position -= self.speed
        elif self.position <= 100:
            self.position += self.speed
    def takeDamage(self, amount:int):
        self.health -= amount
        if self.health <= 0:
            self.dead = True
    def attack(self, target : "Units"):
        self.aCounter += 1
        if self.aCounter % self.attackRate == 0:
            target.takeDamage(self.damage)
    def getTarget(self, enemies : list["Units"]):
        if self.side:
            min = 0 # minimal distance from "me" 
        else:
            min = 100
        closest = None
        for enemy in enemies: # enemies is placeholder, list of enemy units
            if not enemy.dead:
                if self.side:
                    if enemy.position > min and 0 <= self.position - enemy.position <= self.range:
                        closest = enemy
                        min = enemy.position
                        break
                else:
                    if enemy.position < min and 0 <= enemy.position - self.position <= self.range:
                        closest = enemy
                        min = enemy.position
                        break
        if closest == None:
            if self.side:
                if self.position <= self.range:
                    closest = 'A'
            elif 100 - self.position <= self.range:
                closest = 'B'
        return closest
    def attackTower(): # placeholder
        pass
    def update(self, enemies : list["Units"]) -> int:
        # pass a list of enemy units to this function
        if self.curTarget != None:
            if self.curTarget == 'A' or self.curTarget == 'B':
                return self.damage
            else:
                self.attack(self, self.curTarget)
                if self.curTarget.dead:
                    self.curTarget = None
        else:
            self.curTarget = self.getTarget(enemies)
            if self.curTarget == None:
                self.move(self)
        return 0
