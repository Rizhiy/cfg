from __future__ import annotations

from pathlib import Path

from pycs.transforms import LoadFromFile
from tests.data.base_cfg import schema as base_schema

schema = base_schema.inherit()
schema.add_transform(LoadFromFile(Path(__file__).parent / "extra.yaml", require=True))
