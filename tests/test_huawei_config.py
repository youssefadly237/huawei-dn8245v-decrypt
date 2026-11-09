#!/usr/bin/env python3
"""Tests for huawei_config.py — run with:  uv run python tests/test_huawei_config.py"""

import contextlib
import importlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # repo root
import huawei_config as m


def test_every_subcommand_resolves_to_a_callable():
    for command, spec in m.TOOLS.items():
        module_name, _, func_name = spec.partition(":")
        module = importlib.import_module(module_name)
        assert callable(getattr(module, func_name)), f"{command} -> missing {spec}"


def test_no_command_prints_help_and_returns_2():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = m.main([])
    out = buf.getvalue()
    assert rc == 2
    assert "usage: huawei-config" in out
    for command in m.TOOLS:
        assert command in out


def test_unknown_command_returns_2():
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        rc = m.main(["nonsense"])
    assert rc == 2
    assert "invalid choice" in err.getvalue()


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"  ok  {t.__name__}")
    print(f"\n{len(tests)} tests passed")
