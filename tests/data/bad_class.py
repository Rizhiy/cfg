from . import good
from ntc import CN


class BadClass:
    pass


cfg = CN(good.cfg)

cfg.CLASS = BadClass()
