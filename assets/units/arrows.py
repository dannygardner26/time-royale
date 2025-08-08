from assets.units import spells

class Arrows(spells.Spells):
    def __init__(self, location, side=False):
        super().__init__("assets/images/arrows.png", 36, 70, location, side=side)