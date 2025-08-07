from assets.units import units


class Goblin(units.Units):
    def __init__(self, yShift, side):
        super().__init__(yShift, "assets/images/goblinframe1.png", 20, 12, 33, 10, 5, side, size=(40, 60))
