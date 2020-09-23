from ntc import CN

from .base_cfg import cfg as bc

cfg = CN(bc)
cfg.NAME = "Name"


def validate(cfg: CN):
    assert cfg.NAME != "Name"


cfg.validate = validate
