from assets.units import units


class CannonCart(units.Units):
    def __init__(self, yShift, side):
        super().__init__(yShift, "assets/images/cannoncart.png", 180, 21, 27, 5, 110, side, size=(60, 60))
