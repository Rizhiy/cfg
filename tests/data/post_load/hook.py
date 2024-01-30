from __future__ import annotations

from pycs import CN

from ..base_cfg import schema


def hook(cfg: CN) -> None:
    print(cfg.NAME)


schema = schema.inherit()

schema.add_hook(hook)
