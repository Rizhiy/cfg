from __future__ import annotations

import pickle

from ntc import CL, CN


def test_leaf_pickle():
    leaf = CL(str)

    pickled = pickle.dumps(leaf)
    unpickled = pickle.loads(pickled)
    assert unpickled == leaf
    assert unpickled._full_key == leaf._full_key


def test_node_pickle():
    node = CN()
    node.STR = CL(str)
    node.INT = CL(42)
    node.freeze_schema()

    pickled = pickle.dumps(node)
    unpickled = pickle.loads(pickled)

    assert unpickled == node
    for attr_name in node._BUILT_IN_ATTRS:
        assert getattr(node, attr_name) == getattr(unpickled, attr_name)
