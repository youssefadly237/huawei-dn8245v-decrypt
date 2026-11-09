#!/usr/bin/env python3
"""
One entry point for the Huawei DN8245V config toolkit.

    huawei-config fetch    config.bin
    huawei-config decrypt  config.bin config.xml
    huawei-config dump     --file config.xml wifi wan
    huawei-config diff     old.xml new.xml

From a checkout, run it with `uv run huawei-config ...` (or
`python3 huawei_config.py ...`). The individual tools also stay runnable on
their own, e.g. `uv run python tools/decrypt_dn8245v.py ...`.
"""

import argparse
import importlib
import sys

# command -> "module:function". Imports are lazy so commands that do not touch
# crypto still work in an environment without pycryptodome.
TOOLS = {
    "fetch": "tools.fetch_config:main",
    "decrypt": "tools.decrypt_dn8245v:main",
    "dump": "tools.router_dump:main",
    "diff": "tools.config_diff:main",
}


def build_parser():
    parser = argparse.ArgumentParser(
        prog="huawei-config",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Run 'huawei-config COMMAND --help' for command-specific options.",
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND", title="commands")
    sub.add_parser("fetch", help="download the encrypted backup from the router", add_help=False)
    sub.add_parser("decrypt", help="decrypt a backup to plaintext XML", add_help=False)
    sub.add_parser("dump", help="print the settings as readable sections", add_help=False)
    sub.add_parser("diff", help="compare two decrypted configs", add_help=False)
    return parser


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    if not argv:
        parser.print_help()
        return 2

    try:
        args, rest = parser.parse_known_args(argv)
    except SystemExit as exc:  # argparse already printed help or an error
        return exc.code if isinstance(exc.code, int) else 2

    spec = TOOLS.get(args.command)
    if spec is None:
        parser.print_help()
        return 2

    module_name, _, func_name = spec.partition(":")
    func = getattr(importlib.import_module(module_name), func_name)
    return func(rest)


if __name__ == "__main__":
    raise SystemExit(main())
