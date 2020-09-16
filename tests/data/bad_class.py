from .good import defaults


class BadClass:
    pass

cfg = defaults()
cfg.CLASS = BadClass()
