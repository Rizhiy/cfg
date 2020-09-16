from .base_cfg import defaults


class BadClass:
    pass

cfg = defaults()
cfg.CLASSES.ONE = BadClass()
