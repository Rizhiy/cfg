from __future__ import annotations

from pycs.node import CN

from ..base_cfg import schema

schema = schema.inherit()

sub_cfg = CN()
sub_cfg.BAR = "bar"
sub_cfg.FOO = "foo"

schema.FOO = sub_cfg
