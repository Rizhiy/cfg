from ntc import CN
from tests.data.base_cfg import cfg

cfg = cfg.inherit()

cfg = CN(cfg)
cfg.DESCRIBED = "overrided"
