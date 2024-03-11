from __future__ import annotations

import pickle

from pycs import CL, CN

# ruff: noqa


def test_leaf_pickle():
    leaf = CL(str)

    unpickled = pickle.loads(pickle.dumps(leaf))
    assert unpickled == leaf


def test_node_pickle():
    node = CN()
    node.STR = CL(str)
    node.INT = CL(42)
    node.freeze_schema()

    unpickled = pickle.loads(pickle.dumps(node))

    assert unpickled == node
    for attr_name in node._BUILT_IN_ATTRS:  # noqa: SLF001
        assert getattr(node, attr_name) == getattr(unpickled, attr_name)
    assert unpickled.get_raw("STR").full_key == node.get_raw("STR").full_key
