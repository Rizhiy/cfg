from ntc import CN

from .validate import cfg as bc


def validate(cfg: CN) -> None:
    assert cfg.NAME == "Name"


cfg = CN(bc, validators=[validate])
cfg.NAME = "Name"
