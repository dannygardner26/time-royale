from assets.units import units


class Archer(units.Units):
    def __init__(self, yShift, side, start=None):
        super().__init__(yShift, "assets/images/archersframe1.png", 30, 11, 27, 5, 100, side, start=start)
