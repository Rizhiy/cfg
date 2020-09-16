from .good import BaseClass, defaults


class SubClass(BaseClass):
    pass


cfg = defaults()
cfg.CLASS = SubClass()
