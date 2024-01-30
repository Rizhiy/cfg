from __future__ import annotations

from pycs import CN

from .hook import schema


def hook(cfg: CN) -> None:
    print(cfg.NAME + "Inherit")


schema = schema.inherit()
schema.NAME = "Name"

schema.add_hook(hook)
