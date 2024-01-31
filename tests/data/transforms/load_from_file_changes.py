from __future__ import annotations

from tests.data.transforms.load_from_file import schema

cfg = schema.init_cfg()
cfg.DICT.FOO = "Foo value from changes"
cfg.DICT.FOO2 = "Foo2 value from changes"
