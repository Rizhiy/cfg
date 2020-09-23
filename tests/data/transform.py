from ntc import CN

from .base_cfg import cfg


def transform(cfg: CN) -> None:
    if cfg.DICT.FOO == "foo":
        cfg.DICT.FOO = "bar"


cfg = CN(cfg, transforms=[transform])
cfg.NAME = "Name"
