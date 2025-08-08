from assets.units import units


class Splash(units.Units):
    def __init__(self, yShift: float, imagePath: str, health: int, damage: int, attackRate: int, speed: int, range: int,
                 splash: int, side: bool, start=None, size=(60, 90)):
        super().__init__(yShift, imagePath, health, damage, attackRate, speed, range, side, start=start, size=size)
        self.splash = splash

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
