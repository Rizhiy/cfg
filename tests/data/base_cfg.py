from nt_config import CL, CN


class BaseClass:
    pass


cfg = CN()

cfg.DICT = CN()
cfg.DICT.INT = 1
cfg.DICT.FOO = "foo"
cfg.NAME = CL(None, str, required=True)
cfg.LIST = [1, 2, 3, 4]
cfg.CLASS = BaseClass()
cfg.CLASSES = CN(CL(None, BaseClass))
