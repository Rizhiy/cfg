from ntc import CN

from .transform import cfg


def transform(cfg: CN) -> None:
    if cfg.DICT.FOO == "bar":
        cfg.DICT.FOO = "baz"


cfg = CN(cfg, transforms=[transform])
cfg.NAME = "Name"
