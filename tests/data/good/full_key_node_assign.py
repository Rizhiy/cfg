from ntc.node import CN

from ..base_cfg import cfg

cfg = cfg.inherit()

foo = CN()
foo.BAR = "bar"
foo.FOO = "foo"

cfg.FOO = foo
