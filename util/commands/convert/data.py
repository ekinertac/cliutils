import re
import sys


def parse_size(value):
    """Parse data size input and return bytes."""
    value = value.strip().upper()

    # Try to parse with unit suffix
    match = re.match(r"^([\d.]+)\s*([KMGT]?B?)$", value, re.IGNORECASE)
    if match:
        num_str, unit = match.groups()
        num = float(num_str)
        unit = unit.upper()

        if unit in ["", "B"]:
            return int(num)
        elif unit in ["K", "KB"]:
            return int(num * 1024)
        elif unit in ["M", "MB"]:
            return int(num * 1024 * 1024)
        elif unit in ["G", "GB"]:
            return int(num * 1024 * 1024 * 1024)
        elif unit in ["T", "TB"]:
            return int(num * 1024 * 1024 * 1024 * 1024)

    # Try plain number (assume bytes)
    try:
        return int(float(value))
    except ValueError:
        return None


def format_bytes(bytes_val, target_unit):
    """Format bytes to target unit."""
    target_unit = target_unit.lower()

    if target_unit in ["b", "bytes"]:
        return f"{bytes_val} B"
    elif target_unit in ["kb", "k"]:
        return f"{bytes_val / 1024:.2f} KB"
    elif target_unit in ["mb", "m"]:
        return f"{bytes_val / (1024 * 1024):.2f} MB"
    elif target_unit in ["gb", "g"]:
        return f"{bytes_val / (1024 * 1024 * 1024):.2f} GB"
    elif target_unit in ["tb", "t"]:
        return f"{bytes_val / (1024 * 1024 * 1024 * 1024):.2f} TB"
    elif target_unit in ["auto", "smart"]:
        # Automatically choose best unit
        if bytes_val < 1024:
            return f"{bytes_val} B"
        elif bytes_val < 1024 * 1024:
            return f"{bytes_val / 1024:.2f} KB"
        elif bytes_val < 1024 * 1024 * 1024:
            return f"{bytes_val / (1024 * 1024):.2f} MB"
        elif bytes_val < 1024 * 1024 * 1024 * 1024:
            return f"{bytes_val / (1024 * 1024 * 1024):.2f} GB"
        else:
            return f"{bytes_val / (1024 * 1024 * 1024 * 1024):.2f} TB"
    else:
        print(f"Error: Unsupported target unit '{target_unit}'", file=sys.stderr)
        sys.exit(1)


def handle_command(args):
    """Handle data size conversion command."""
    bytes_val = parse_size(args.value)
    if bytes_val is None:
        print(f"Error: Unable to parse data size '{args.value}'", file=sys.stderr)
        sys.exit(1)

    result = format_bytes(bytes_val, args.target)
    print(result)


def setup_parser(subparsers):
    """Setup data size conversion subparser."""
    data_parser = subparsers.add_parser(
        "data",
        help="Convert data sizes",
        description="Convert between bytes, KB, MB, GB, TB.",
    )
    data_parser.add_argument(
        "value", type=str, help="Data size value (e.g., 1024, 1KB, 1.5MB)"
    )
    data_parser.add_argument(
        "target",
        type=str,
        help="Target unit: bytes, kb, mb, gb, tb, auto",
    )
    data_parser.set_defaults(func=handle_command)
