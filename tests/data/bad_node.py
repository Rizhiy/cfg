from ntc import CN

from .base_cfg import cfg


class BadClass:
    pass


cfg = CN(cfg)

cfg.NAME = "bad_node"

cfg.CLASSES.ONE = BadClass()
