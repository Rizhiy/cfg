from .base_cfg import defaults


class BadClass:
    pass


cfg = defaults()

cfg.NAME = "bad_node"

cfg.CLASSES.ONE = BadClass()
