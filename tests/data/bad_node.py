from . import base_cfg
from ntc import CN


class BadClass:
    pass


cfg = CN(base_cfg.cfg)

cfg.NAME = "bad_node"

cfg.CLASSES.ONE = BadClass()
