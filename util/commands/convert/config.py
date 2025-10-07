import json
import os
import sys


def parse_config(data, format_type):
    """Parse config data from specified format."""
    format_type = format_type.lower()

    try:
        if format_type == "json":
            return json.loads(data)
        elif format_type == "yaml":
            try:
                import yaml
            except ImportError:
                print(
                    "Error: PyYAML not installed. Install with: pip install PyYAML",
                    file=sys.stderr,
                )
                sys.exit(1)
            return yaml.safe_load(data)
        elif format_type == "toml":
            try:
                import tomli
            except ImportError:
                print(
                    "Error: tomli not installed. Install with: pip install tomli",
                    file=sys.stderr,
                )
                sys.exit(1)
            return tomli.loads(data)
        elif format_type == "xml":
            try:
                import xmltodict
            except ImportError:
                print(
                    "Error: xmltodict not installed. Install with: pip install xmltodict",
                    file=sys.stderr,
                )
                sys.exit(1)
            return xmltodict.parse(data)
        else:
            print(f"Error: Unsupported format '{format_type}'", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error parsing {format_type}: {e}", file=sys.stderr)
        sys.exit(1)


def serialize_config(data, format_type):
    """Serialize config data to specified format."""
    format_type = format_type.lower()

    try:
        if format_type == "json":
            return json.dumps(data, indent=2, ensure_ascii=False)
        elif format_type == "yaml":
            try:
                import yaml
            except ImportError:
                print(
                    "Error: PyYAML not installed. Install with: pip install PyYAML",
                    file=sys.stderr,
                )
                sys.exit(1)
            return yaml.dump(data, default_flow_style=False, allow_unicode=True)
        elif format_type == "toml":
            try:
                import tomli_w
            except ImportError:
                print(
                    "Error: tomli-w not installed. Install with: pip install tomli-w",
                    file=sys.stderr,
                )
                sys.exit(1)
            return tomli_w.dumps(data)
        elif format_type == "xml":
            try:
                import xmltodict
            except ImportError:
                print(
                    "Error: xmltodict not installed. Install with: pip install xmltodict",
                    file=sys.stderr,
                )
                sys.exit(1)
            return xmltodict.unparse(data, pretty=True)
        else:
            print(f"Error: Unsupported format '{format_type}'", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error serializing to {format_type}: {e}", file=sys.stderr)
        sys.exit(1)


def detect_format(filename):
    """Detect config format from file extension."""
    ext = os.path.splitext(filename)[1].lower()

    if ext in [".json"]:
        return "json"
    elif ext in [".yaml", ".yml"]:
        return "yaml"
    elif ext in [".toml"]:
        return "toml"
    elif ext in [".xml"]:
        return "xml"
    else:
        return None


def handle_command(args):
    """Handle config conversion command."""
    input_file = args.input_file
    target_format = args.target_format.lower()

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found", file=sys.stderr)
        sys.exit(1)

    # Detect input format
    input_format = detect_format(input_file)
    if input_format is None:
        print(
            "Error: Cannot detect format from file extension. Supported: .json, .yaml, .yml, .toml, .xml",
            file=sys.stderr,
        )
        sys.exit(1)

    # Validate target format
    if target_format not in ["json", "yaml", "toml", "xml"]:
        print(
            f"Error: Unsupported target format '{target_format}'. Use: json, yaml, toml, xml",
            file=sys.stderr,
        )
        sys.exit(1)

    # Read input file
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            input_data = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse input format
    parsed_data = parse_config(input_data, input_format)

    # Convert to target format
    output_data = serialize_config(parsed_data, target_format)

    # Print to stdout
    print(output_data)


def setup_parser(subparsers):
    """Setup config conversion subparser."""
    config_parser = subparsers.add_parser(
        "config",
        help="Convert config file formats",
        description="Convert between JSON, YAML, TOML, and XML configuration files.",
    )
    config_parser.add_argument("input_file", type=str, help="Input config file")
    config_parser.add_argument(
        "target_format",
        type=str,
        choices=["json", "yaml", "toml", "xml"],
        help="Target format",
    )
    config_parser.set_defaults(func=handle_command)
