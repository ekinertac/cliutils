import csv
import json
import os
import sys


def csv_to_json(csv_file):
    """Convert CSV to JSON."""
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return json.dumps(data, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error converting CSV to JSON: {e}", file=sys.stderr)
        sys.exit(1)


def json_to_csv(json_file):
    """Convert JSON to CSV."""
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Handle both array of objects and single object
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            print(
                "Error: JSON must be an array of objects or a single object",
                file=sys.stderr,
            )
            sys.exit(1)

        if not data:
            return ""

        # Get all unique keys from all objects
        keys = set()
        for item in data:
            if isinstance(item, dict):
                keys.update(item.keys())
            else:
                print("Error: JSON array must contain objects", file=sys.stderr)
                sys.exit(1)

        keys = sorted(keys)

        # Write CSV
        output = []
        output.append(",".join(keys))

        for item in data:
            row = []
            for key in keys:
                value = item.get(key, "")
                # Handle nested objects/arrays
                if isinstance(value, (dict, list)):
                    value = json.dumps(value)
                else:
                    value = str(value)
                # Escape quotes and wrap in quotes if contains comma or quote
                if "," in value or '"' in value or "\n" in value:
                    value = '"' + value.replace('"', '""') + '"'
                row.append(value)
            output.append(",".join(row))

        return "\n".join(output)
    except Exception as e:
        print(f"Error converting JSON to CSV: {e}", file=sys.stderr)
        sys.exit(1)


def csv_to_markdown(csv_file):
    """Convert CSV to Markdown table."""
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        if not rows:
            return ""

        # Header
        header = rows[0]
        output = ["| " + " | ".join(header) + " |"]
        output.append("| " + " | ".join(["---"] * len(header)) + " |")

        # Data rows
        for row in rows[1:]:
            # Pad row if it's shorter than header
            while len(row) < len(header):
                row.append("")
            output.append("| " + " | ".join(row[: len(header)]) + " |")

        return "\n".join(output)
    except Exception as e:
        print(f"Error converting CSV to Markdown: {e}", file=sys.stderr)
        sys.exit(1)


def json_to_markdown(json_file):
    """Convert JSON to Markdown table."""
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Handle both array of objects and single object
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            print(
                "Error: JSON must be an array of objects or a single object",
                file=sys.stderr,
            )
            sys.exit(1)

        if not data:
            return ""

        # Get all unique keys
        keys = set()
        for item in data:
            if isinstance(item, dict):
                keys.update(item.keys())
        keys = sorted(keys)

        # Header
        output = ["| " + " | ".join(keys) + " |"]
        output.append("| " + " | ".join(["---"] * len(keys)) + " |")

        # Data rows
        for item in data:
            row = []
            for key in keys:
                value = item.get(key, "")
                if isinstance(value, (dict, list)):
                    value = json.dumps(value)
                else:
                    value = str(value)
                row.append(value)
            output.append("| " + " | ".join(row) + " |")

        return "\n".join(output)
    except Exception as e:
        print(f"Error converting JSON to Markdown: {e}", file=sys.stderr)
        sys.exit(1)


def handle_command(args):
    """Handle tabular data conversion command."""
    input_file = args.input_file
    target_format = args.target_format.lower()

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found", file=sys.stderr)
        sys.exit(1)

    # Detect input format
    ext = os.path.splitext(input_file)[1].lower()

    # Perform conversion
    if ext == ".csv":
        if target_format in ["json"]:
            result = csv_to_json(input_file)
        elif target_format in ["markdown", "md", "table"]:
            result = csv_to_markdown(input_file)
        else:
            print(f"Error: Cannot convert CSV to '{target_format}'", file=sys.stderr)
            print("Supported: json, markdown", file=sys.stderr)
            sys.exit(1)
    elif ext == ".json":
        if target_format in ["csv"]:
            result = json_to_csv(input_file)
        elif target_format in ["markdown", "md", "table"]:
            result = json_to_markdown(input_file)
        else:
            print(f"Error: Cannot convert JSON to '{target_format}'", file=sys.stderr)
            print("Supported: csv, markdown", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Error: Unsupported input format '{ext}'", file=sys.stderr)
        print("Supported: .csv, .json", file=sys.stderr)
        sys.exit(1)

    print(result)


def setup_parser(subparsers):
    """Setup tabular data conversion subparser."""
    tabular_parser = subparsers.add_parser(
        "tabular",
        aliases=["table"],
        help="Convert tabular data formats",
        description="Convert between CSV, JSON, and Markdown tables.",
    )
    tabular_parser.add_argument(
        "input_file",
        type=str,
        help="Input file (CSV or JSON)",
    )
    tabular_parser.add_argument(
        "target_format",
        type=str,
        choices=["csv", "json", "markdown", "md", "table"],
        help="Target format",
    )
    tabular_parser.set_defaults(func=handle_command)
