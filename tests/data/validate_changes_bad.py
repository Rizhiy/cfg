from ntc import CN

from .validate import cfg

cfg = CN(cfg)
cfg.NAME = "Name"


def validate(cfg: CN):
    assert cfg.NAME == "Name"


cfg.add_validator(validate)
