from typing import Union

from assets.units import units


class Giant(units.Units):
    def __init__(self, yShift, side):
        super().__init__(yShift, "assets/images/giantframe1.png", 200, 25, 45, 4, 12, side, size=(100, 150))

    def getTarget(self, enemies: list[units.Units]) -> Union[units.Units, str]:
        if self.side:
            if self.position - 100 <= self.range:
                return 'A'
        elif 820 - self.position <= self.range:
            return 'B'
