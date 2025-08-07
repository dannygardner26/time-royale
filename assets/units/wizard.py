from assets.units import units


class Wizard(units.Units):
    def __init__(self, yShift, side):
        super().__init__(yShift, "assets/images/wizard.png", 75, 28, 42, 5, 110, side, size=(80, 80))
        self.splash = 30

    def attack(self, target: units.Units, enemies: list[units.Units]):
        self.aCounter += 1
        if self.aCounter % self.attackRate == 0:
            # Normal attack
            target.takeDamage(self.damage)
            # Add bonus splash damage
            splashCenter = self.curTarget.position
            for enemy in enemies:
                if not enemy.dead:
                    if self.side:
                        if -self.splash <= splashCenter - enemy.position <= self.splash:
                            enemy.takeDamage(self.damage / 2)
                    else:
                        if -self.splash <= enemy.position - splashCenter <= self.splash:
                            enemy.takeDamage(self.damage / 2)
