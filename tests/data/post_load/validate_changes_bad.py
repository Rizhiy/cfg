from ntc import CN

from .validate import cfg

cfg = CN(cfg)
cfg.REQUIRED = "Required"


def validate(cfg: CN):
    assert cfg.NAME == "Name"


cfg.add_validator(validate)
