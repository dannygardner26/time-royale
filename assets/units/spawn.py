from assets.units import units, spells


class Spawn(spells.Spells):
    def __init__(self, image_path: str, damage: int, radius: int, location: int, spawn: list[units.Units],
                 side=False, size=(250, 320)):
        super().__init__(image_path, damage, radius, location, side, size=size)
        self.radius = radius
        self.spawn = spawn

    def spawnUnits(self, addTo: list[units.Units]):
        addTo += self.spawn
        return addTo
