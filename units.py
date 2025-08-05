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
        self.position = 100+800*side
        self.side = side
        self.attackRate = attackRate
        self.aCounter = 0
        self.curTarget = None
    def move(self):
        # change position
        if self.side and self.position >= 100:
            self.position -= self.speed
        elif self.position <= 900:
            self.position += self.speed
    def takeDamage(self, amount:int):
        self.health -= amount
        if self.health <= 0:
            self.dead = True
            print(self.id, "deaded")
    def attack(self, target : "Units"):
        self.aCounter += 1
        if self.aCounter % self.attackRate == 0:
            target.takeDamage(self.damage)
    def getTarget(self, enemies : list["Units"]):
        if self.side:
            min = 100 # minimal distance from "me" 
        else:
            min = 900
        closest = None
        for enemy in enemies: # enemies is placeholder, list of enemy units
            if not enemy.dead:
                if self.side:
                    if enemy.position > min and self.position - enemy.position <= self.range:
                        closest = enemy
                        min = enemy.position
                else:
                    if enemy.position < min and enemy.position - self.position <= self.range:
                        closest = enemy
                        min = enemy.position
        if closest == None:
            if self.side:
                if self.position - 100 <= self.range:
                    closest = 'A'
            elif 900 - self.position <= self.range:
                closest = 'B'
        return closest
    def attackTower(): # placeholder
        pass
    def update(self, enemies : list["Units"]) -> int:
        # pass a list of enemy units to this function
        if not self.dead:
            if self.curTarget != None:
                if self.curTarget == 'A' or self.curTarget == 'B':
                    self.aCounter += 1
                    if self.aCounter % self.attackRate == 0:
                        return self.damage
                else:
                    self.attack(self.curTarget)
                    if self.curTarget.dead:
                        self.curTarget = None
            else:
                self.curTarget = self.getTarget(enemies)
                print(self.id, self.curTarget)
                if self.curTarget == None:
                    self.move()
        return 0
