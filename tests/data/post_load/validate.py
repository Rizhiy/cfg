from __future__ import annotations

from ntc import CN

from ..base_cfg import cfg


def validate(cfg: CN) -> None:
    assert cfg.NAME != "Name"


cfg = cfg.inherit()
cfg.NAME = "Name"

cfg.add_validator(validate)
