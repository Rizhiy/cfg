from .good import cfg
from ntc import CN


class BadClass:
    pass


cfg = CN(cfg)

cfg.CLASS = BadClass()
