from ntc import CN

from .base_cfg import cfg


class BadSubClass:
    pass


cfg = CN(cfg)
cfg.NAME = "bad_node"
cfg.SUBCLASSES.ONE = BadSubClass
