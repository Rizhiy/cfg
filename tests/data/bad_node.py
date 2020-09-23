from ntc import CN

from .good import cfg


class BadClass:
    pass


cfg = CN(cfg)
cfg.CLASSES.ONE = BadClass()
