from assets.units import splash


class Valkyrie(splash.Splash):
    def __init__(self, yShift, side):
        super().__init__(yShift, "assets/images/valkyrie.png", 190, 26, 45, 5, 12, 40, side, size=(70, 70))
