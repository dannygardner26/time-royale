from typing import Union

from assets.units import tpriority


class Giant(tpriority.tPriority):
    def __init__(self, yShift, side, start=None):
        super().__init__(yShift, "assets/images/giantframe1.png", 200, 25, 45, 4, 12, side, size=(100, 150), start=start)

