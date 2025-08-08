from assets.units import units

class Spells(units.Units):
    def __init__(self, image_path: str, damage: int, radius: int, location: int, spawn: list[units.Units]=False, side=False):
        super().__init__(0, image_path, 999999999, damage, 0, 0, 0, radius, side, start=location, size=(70, 70))
        self.spawn = spawn

    def attack(self, enemies: list[units.Units]):
        for enemy in enemies:
            if not enemy.dead:
                if abs(self.position - enemy.position) <= self.range:
                    enemy.takeDamage(self.damage)
    def update(self, enemies):
        tower = 0
        self.attack(enemies)
        if self.side:
            if self.position - 100 <= self.radius:
                tower = self.damage
            else:
                if 820 - self.position <= self.radius:
                    tower = self.damage
        if self.spawn is not None:
            return tower, self.spawn
        else:
            return tower, []
