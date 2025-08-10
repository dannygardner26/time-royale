from assets.units import spawn, goblin
import random


class GoblinBarrel(spawn.Spawn):
    def __init__(self, location, side=False):
        spawns = [goblin.Goblin(random.random(), side, start=location), goblin.Goblin(random.random(), side, start=location)]
        super().__init__("assets/images/goblinbarrel.png", 0, 0, location, spawns, side=side, size=(60, 60))
