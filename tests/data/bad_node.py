from .base_cfg import cfg, BaseClass


class BadClass:
    pass


cfg.CLASSES.ONE = BadClass()
