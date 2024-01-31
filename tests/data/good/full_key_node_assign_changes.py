from __future__ import annotations

from tests.data.good.full_key_node_assign import schema

cfg = schema.init_cfg()

cfg.FOO.BAR = "foo"
