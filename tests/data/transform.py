from ntc import CN

from .base_cfg import cfg as bc

cfg = CN(bc)
cfg.NAME = "Name"


def transform(cfg: CN):
    if cfg.DICT.FOO == "foo":
        cfg.DICT.FOO = "bar"


cfg.transform = transform
