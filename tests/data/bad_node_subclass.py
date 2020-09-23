from ntc import CN

from .good import cfg


class BadSubClass:
    pass


cfg = CN(cfg)
cfg.SUBCLASSES.ONE = BadSubClass
