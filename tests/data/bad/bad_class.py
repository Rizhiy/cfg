from ntc import CN

from ..good.good import cfg


class BadClass:
    pass


cfg = CN(cfg)

cfg.CLASS = BadClass()
