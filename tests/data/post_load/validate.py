from ntc import CN

from ..base_cfg import cfg


def validate(cfg: CN) -> None:
    assert cfg.NAME != "Name"


cfg = cfg.clone()
cfg.NAME = "Name"

cfg.add_validator(validate)
