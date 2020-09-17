from .good import cfg
from .base_cfg import BaseClass
from ntc import CN


cfg = CN(cfg)
cfg.CLASSES.ONE = BaseClass()
