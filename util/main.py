import argparse
import importlib
import pkgutil
import sys

import util.commands

def main():
    parser = argparse.ArgumentParser(prog='util', description='A collection of utility commands.')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Discover and load commands
    for _, name, _ in pkgutil.iter_modules(util.commands.__path__):
        module = importlib.import_module(f'util.commands.{name}')
        if hasattr(module, 'setup_parser'):
            module.setup_parser(subparsers)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
