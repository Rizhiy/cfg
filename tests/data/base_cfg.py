from nt_config import CL, CN


class BaseClass:
    pass


_cfg = CN()

_cfg.DICT = CN()
_cfg.DICT.INT = 1
_cfg.DICT.FOO = "foo"
_cfg.NAME = CL(None, str, required=True)
_cfg.LIST = [1, 2, 3, 4]
_cfg.CLASS = BaseClass()
_cfg.CLASSES = CN(CL(None, BaseClass))

def defaults():
    return _cfg.clone()

__all__ = ["defaults"]


