from ntc import CN
from tests.data.base_class import BaseClass
from tests.data.required.bad_inherit import cfg

cfg = CN(cfg)
cfg.REQUIRED_CLASSES.TWO = BaseClass()
