from .base_cfg import cfg


class BadClass:
    pass


cfg.CLASSES.ONE = BadClass()
