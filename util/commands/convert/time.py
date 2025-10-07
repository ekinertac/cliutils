import sys
from datetime import datetime


def convert(from_format, value, to_format):
    """Convert time between formats."""
    from_format = from_format.lower()
    to_format = to_format.lower()

    try:
        # Parse input
        if from_format in ["unix", "timestamp", "epoch"]:
            dt = datetime.fromtimestamp(int(value))
        elif from_format in ["iso", "iso8601", "datetime"]:
            # Try to parse ISO format
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        elif from_format == "now":
            dt = datetime.now()
        else:
            print(f"Error: Unsupported source format '{from_format}'", file=sys.stderr)
            sys.exit(1)

        # Convert to target format
        if to_format in ["unix", "timestamp", "epoch"]:
            return str(int(dt.timestamp()))
        elif to_format in ["iso", "iso8601"]:
            return dt.isoformat()
        elif to_format in ["date"]:
            return dt.strftime("%Y-%m-%d")
        elif to_format in ["time"]:
            return dt.strftime("%H:%M:%S")
        elif to_format in ["datetime"]:
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            print(f"Error: Unsupported target format '{to_format}'", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_command(args):
    """Handle time conversion command."""
    result = convert(args.from_format, args.value, args.to_format)
    print(result)


def setup_parser(subparsers):
    """Setup time conversion subparser."""
    time_parser = subparsers.add_parser(
        "time",
        help="Convert time formats",
        description="Convert between Unix timestamp, ISO format, and datetime.",
    )
    time_parser.add_argument(
        "from_format", type=str, help="Source format: unix, iso, now"
    )
    time_parser.add_argument("value", type=str, help="Time value to convert")
    time_parser.add_argument(
        "to_format",
        type=str,
        help="Target format: unix, iso, date, time, datetime",
    )
    time_parser.set_defaults(func=handle_command)
