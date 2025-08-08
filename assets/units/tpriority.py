from typing import Union

from assets.units import units


class tPriority(units.Units):
    def __init__(self, yShift: float, imagePath: str, health: int, damage: int, attackRate: int, speed: int, range: int,
                 side: bool, start=None, size=(60, 90)):
        super().__init__(yShift, imagePath, health, damage, attackRate, speed, range, side, start=start, size=size)

    def getTarget(self, enemies: list[units.Units]) -> Union[units.Units, str]:
        if self.side:
            if self.position - 100 <= self.range:
                return 'A'
        elif 820 - self.position <= self.range:
            return 'B'
