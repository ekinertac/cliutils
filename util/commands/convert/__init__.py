"""
Convert command module.
Handles conversions between different formats: colors, bases, data sizes, time, files, configs, documents, text, and tabular data.
"""

from . import base, color, config, data, document, file, tabular, text, time


def setup_parser(subparsers):
    """Setup the main convert parser and all conversion subparsers."""
    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert between different formats",
        description="Convert colors, number bases, data sizes, time formats, file formats, config files, documents, text encodings, and tabular data.",
    )
    convert_subparsers = convert_parser.add_subparsers(
        dest="convert_type", required=True, help="Type of conversion"
    )

    # Setup each conversion type subparser
    color.setup_parser(convert_subparsers)
    base.setup_parser(convert_subparsers)
    data.setup_parser(convert_subparsers)
    time.setup_parser(convert_subparsers)
    file.setup_parser(convert_subparsers)
    config.setup_parser(convert_subparsers)
    document.setup_parser(convert_subparsers)
    text.setup_parser(convert_subparsers)
    tabular.setup_parser(convert_subparsers)
