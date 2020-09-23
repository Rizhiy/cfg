from ntc import CL, CN


class BaseClass:
    def __eq__(self, other):
        return True


cfg = CN()

cfg.DICT = CN()
cfg.DICT.INT = 1
cfg.DICT.FOO = "foo"
cfg.DICT.X = "X"
cfg.NAME = CL(None, str, required=True)
cfg.LIST = [1, 2, 3, 4]
cfg.CLASS = BaseClass()
cfg.CLASSES = CN(BaseClass)
cfg.SUBCLASSES = CN(CL(None, BaseClass, subclass=True))


def transform(cfg: CN):
    cfg.DICT.X = "Y"


def validate(cfg: CN):
    assert len(cfg.NAME) > 0


cfg.add_transform(transform)
cfg.add_validator(validate)
