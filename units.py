import pygame


class Units:
    def __init__(self, id: float, image_path: str, health: int, damage: int, attackRate: int, speed: int, range: int,
                 side: bool, start=None):
        self.tpriority = False
        self.splash = 0
        # Set different sizes for different units
        if "knight" in image_path:
            size = (80, 120)  # Make the knight taller (width, height)
        elif "giant" in image_path:
            self.tpriority = True
            size = (100, 150)  # Make the giant bigger
        elif "goblin" in image_path:
            size = (40, 60)  # Goblin smaller
        elif "wizard" in image_path:
            self.splash = 20
            size = None  # Change this
        else:
            size = (60, 90)  # Default size

        img = pygame.image.load(image_path).convert_alpha()
        img = pygame.transform.scale(img, size)
        if side:  # If this is an enemy, flip horizontally
            img = pygame.transform.flip(img, True, False)
        self.image = img

        self.id = id
        self.dead = False
        self.health = health
        self.damage = damage
        self.speed = speed
        self.range = range
        if start is not None:
            self.position = start
        else:
            self.position = 100 + 720 * side
        self.side = side
        self.attackRate = attackRate
        self.aCounter = 0
        self.curTarget = None

    def move(self):
        # change position
        if self.side and self.position >= 100:
            self.position -= self.speed
        elif self.position <= 820:
            self.position += self.speed

    def takeDamage(self, amount: float):
        self.health -= amount
        if self.health <= 0:
            self.dead = True
            # print(self.id, "deaded") # debug code 

    def attack(self, target: "Units", enemies: list["Units"]):
        self.aCounter += 1
        if self.aCounter % self.attackRate == 0:
            target.takeDamage(self.damage)
            if self.splash > 0:
                self.splashAttack(enemies)

    def splashAttack(self, enemies: list["Units"]):
        splashCenter = self.curTarget.position
        for enemy in enemies:
            if not enemy.dead:
                if self.side:
                    if -self.splash <= splashCenter - enemy.position <= self.splash:
                        enemy.takeDamage(self.damage / 2)
                else:
                    if -self.splash <= enemy.position - splashCenter <= self.splash:
                        enemy.takeDamage(self.damage / 2)

    def getTarget(self, enemies: list["Units"]) -> "Units":
        closest = None
        if not self.tpriority:
            if self.side:
                min = 100  # minimal distance from "me"
            else:
                min = 820
            for enemy in enemies:  # enemies is placeholder, list of enemy units
                if not enemy.dead:
                    if self.side:
                        if enemy.position > min and -self.range <= self.position - enemy.position <= self.range:
                            closest = enemy
                            min = enemy.position
                    else:
                        if enemy.position < min and -self.range <= enemy.position - self.position <= self.range:
                            closest = enemy
                            min = enemy.position
        if closest is None:
            if self.side:
                if self.position - 100 <= self.range:
                    closest = 'A'
            elif 820 - self.position <= self.range:
                closest = 'B'
        return closest

    def inRange(self, enemy: "Units") -> bool:
        if self.side:
            if 0 <= self.position - enemy.position <= self.range:
                # print(self.id, "case uno")
                return True
        else:
            if 0 <= enemy.position - self.position <= self.range:
                # print(self.id, "case dos")
                return True
        # print(self.id, "case tres")
        return False

    def update(self, enemies: list["Units"]) -> int:
        # pass a list of enemy units to this function
        if not self.dead:
            if self.curTarget is not None:
                if self.curTarget == 'A' or self.curTarget == 'B':
                    self.aCounter += 1
                    if self.aCounter % self.attackRate == 0:
                        return self.damage
                else:
                    if self.inRange(self.curTarget):
                        # print(self.id, "a")
                        self.attack(self.curTarget, enemies)
                        if self.curTarget.dead:
                            self.curTarget = None
                    else:
                        self.curTarget = None
                        # print(self.id, "b")
            else:
                self.curTarget = self.getTarget(enemies)
                # print(self.id, self.curTarget)
                if self.curTarget is None:
                    self.move()
        return 0
