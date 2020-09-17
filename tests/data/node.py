from . import good
from .base_cfg import BaseClass
from ntc import CN


cfg = CN(good.cfg)
cfg.CLASSES.ONE = BaseClass()
