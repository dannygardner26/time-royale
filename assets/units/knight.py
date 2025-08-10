from assets.units import units


class Knight(units.Units):
    def __init__(self, yShift, side, start=None):
        super().__init__(yShift, "assets/images/knightframe1.png", 170, 20, 36, 5, 12, side, size=(80, 120), start=start)
