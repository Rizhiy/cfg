from __future__ import annotations


def pytest_ignore_collect(path):
    if "tests/data/" in str(path):
        return True
    return False
