import sys


def convert(from_base, value, to_base):
    """Convert number from one base to another."""
    from_base = from_base.lower()
    to_base = to_base.lower()

    # Parse input based on source base
    try:
        if from_base in ["dec", "decimal", "10"]:
            num = int(value, 10)
        elif from_base in ["hex", "hexadecimal", "16"]:
            # Remove 0x prefix if present
            if value.lower().startswith("0x"):
                value = value[2:]
            num = int(value, 16)
        elif from_base in ["bin", "binary", "2"]:
            # Remove 0b prefix if present
            if value.lower().startswith("0b"):
                value = value[2:]
            num = int(value, 2)
        elif from_base in ["oct", "octal", "8"]:
            # Remove 0o prefix if present
            if value.lower().startswith("0o"):
                value = value[2:]
            num = int(value, 8)
        else:
            print(f"Error: Unsupported source base '{from_base}'", file=sys.stderr)
            sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid {from_base} value '{value}': {e}", file=sys.stderr)
        sys.exit(1)

    # Convert to target base
    if to_base in ["dec", "decimal", "10"]:
        return str(num)
    elif to_base in ["hex", "hexadecimal", "16"]:
        return hex(num)[2:]  # Remove 0x prefix
    elif to_base in ["0x", "0xhex"]:
        return hex(num)  # Keep 0x prefix
    elif to_base in ["bin", "binary", "2"]:
        return bin(num)[2:]  # Remove 0b prefix
    elif to_base in ["0b", "0bbin"]:
        return bin(num)  # Keep 0b prefix
    elif to_base in ["oct", "octal", "8"]:
        return oct(num)[2:]  # Remove 0o prefix
    elif to_base in ["0o", "0ooct"]:
        return oct(num)  # Keep 0o prefix
    else:
        print(f"Error: Unsupported target base '{to_base}'", file=sys.stderr)
        sys.exit(1)


def handle_command(args):
    """Handle base conversion command."""
    result = convert(args.from_base, args.value, args.to_base)
    print(result)


def setup_parser(subparsers):
    """Setup base conversion subparser."""
    base_parser = subparsers.add_parser(
        "base",
        help="Convert number bases",
        description="Convert between decimal, hexadecimal, binary, and octal.",
    )
    base_parser.add_argument(
        "from_base", type=str, help="Source base: dec, hex, bin, oct"
    )
    base_parser.add_argument("value", type=str, help="Value to convert")
    base_parser.add_argument(
        "to_base", type=str, help="Target base: dec, hex, bin, oct, 0x, 0b, 0o"
    )
    base_parser.set_defaults(func=handle_command)
