from . import base_cfg
from ntc import CN

cfg = CN(base_cfg.cfg)

cfg.NAME = "bad_attr"

cfg.NEW = "bar"
