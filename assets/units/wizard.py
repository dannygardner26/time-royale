from assets.units import splash


class Wizard(splash.Splash):
    def __init__(self, yShift, side, start=None):
        super().__init__(yShift, "assets/images/wizard.png", 75, 28, 42, 5, 110, 30, side, size=(80, 80), start=start)
