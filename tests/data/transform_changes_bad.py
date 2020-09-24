from ntc import CN

from .transform_inheritance import cfg

cfg = CN(cfg)
cfg.REQUIRED = "Required"


def transform(cfg: CN):
    cfg.NAME = "N"


cfg.add_transform(transform)
