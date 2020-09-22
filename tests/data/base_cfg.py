from ntc import CL, CN


class BaseClass:
    def __eq__(self, other):
        return True


cfg = CN()

cfg.DICT = CN()
cfg.DICT.INT = 1
cfg.DICT.FOO = "foo"
cfg.NAME = CL(None, str, required=True)
cfg.LIST = [1, 2, 3, 4]
cfg.CLASS = BaseClass()
cfg.CLASSES = CN(leaf_spec=CL(None, BaseClass))
cfg.SUBCLASSES = CN(leaf_spec=CL(None, BaseClass, subclass=True))
