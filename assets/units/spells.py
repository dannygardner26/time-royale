from assets.units import units


class Spells(units.Units):
    def __init__(self, image_path: str, damage: int, radius: int, location: int, side=False, size=(250, 320)):
        super().__init__(0, image_path, 999999999, damage, 0, 0, 0,  side, start=location, size=size)
        self.radius = radius

    def attack(self, enemies: list[units.Units]):
        for enemy in enemies:
            if not enemy.dead:
                if abs(self.position - enemy.position) <= self.radius:
                    enemy.takeDamage(self.damage)

    def update(self, enemies: list[units.Units]) -> int:
        tower = 0
        self.attack(enemies)
        if self.side:
            if self.position - 100 <= self.radius:
                tower = self.damage
        else:
            if 820 - self.position <= self.radius:
                tower = self.damage
        self.dead = True
        return tower
