from __future__ import annotations

from pycs.node import CN

from ..base_cfg import cfg

cfg = cfg.inherit()

sub_cfg = CN()
sub_cfg.BAR = "bar"
sub_cfg.FOO = "foo"

cfg.FOO = sub_cfg
