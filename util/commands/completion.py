import argparse
import sys
import subprocess

def completion_command(args):
    if args.shell == 'bash':
        print("To activate autocompletion for bash, add the following to your ~/.bashrc or ~/.bash_profile:")
        print("eval \"$(register-python-argcomplete util)\"")
        print("Then, source your bashrc/bash_profile: source ~/.bashrc")
    elif args.shell == 'zsh':
        print("To activate autocompletion for zsh, add the following to your ~/.zshrc:")
        print("eval \"$(register-python-argcomplete util)\"")
        print("Then, source your zshrc: source ~/.zshrc")
    else:
        print(f"Error: Unsupported shell for autocompletion: {args.shell}")
        sys.exit(1)

def setup_parser(subparsers):
    completion_parser = subparsers.add_parser('completion', help='Generate autocompletion script', description='Generate shell autocompletion script for util.')
    completion_parser.add_argument('shell', choices=['bash', 'zsh'], help='The shell for which to generate completion (bash or zsh)')
    completion_parser.set_defaults(func=completion_command)
