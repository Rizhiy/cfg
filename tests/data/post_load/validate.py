from __future__ import annotations

from pycs import CN

from ..base_cfg import schema


def validate(cfg: CN) -> None:
    assert cfg.NAME != "Name"


schema = schema.inherit()
schema.NAME = "Name"

schema.add_validator(validate)
