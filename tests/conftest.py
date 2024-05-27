from __future__ import annotations


def pytest_ignore_collect(path):
    return "tests/data/" in str(path)
