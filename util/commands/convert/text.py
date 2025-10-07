import html
import os
import sys
import urllib.parse


def url_encode(text):
    """URL encode text."""
    return urllib.parse.quote(text)


def url_decode(text):
    """URL decode text."""
    return urllib.parse.unquote(text)


def html_encode(text):
    """Encode HTML entities."""
    return html.escape(text)


def html_decode(text):
    """Decode HTML entities."""
    return html.unescape(text)


def convert_line_endings(text, target):
    """Convert line endings."""
    target = target.lower()

    # Normalize to LF first
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    if target in ["crlf", "windows", "dos"]:
        return text.replace("\n", "\r\n")
    elif target in ["lf", "unix", "linux", "mac"]:
        return text  # Already LF
    elif target in ["cr", "oldmac"]:
        return text.replace("\n", "\r")
    else:
        print(f"Error: Unsupported line ending format '{target}'", file=sys.stderr)
        sys.exit(1)


def escape_string(text, language):
    """Escape string for programming language."""
    language = language.lower()

    if language in ["python", "py"]:
        # Python string escape
        return repr(text)[1:-1]  # Remove outer quotes from repr
    elif language in ["javascript", "js"]:
        # JavaScript string escape
        escaped = text.replace("\\", "\\\\")
        escaped = escaped.replace('"', '\\"')
        escaped = escaped.replace("'", "\\'")
        escaped = escaped.replace("\n", "\\n")
        escaped = escaped.replace("\r", "\\r")
        escaped = escaped.replace("\t", "\\t")
        return escaped
    elif language in ["sql"]:
        # SQL string escape (double single quotes)
        return text.replace("'", "''")
    elif language in ["json"]:
        import json

        return json.dumps(text)[1:-1]  # Remove outer quotes
    else:
        print(f"Error: Unsupported language '{language}'", file=sys.stderr)
        sys.exit(1)


def unescape_string(text, language):
    """Unescape string from programming language format."""
    language = language.lower()

    if language in ["python", "py", "json"]:
        # Use eval with quotes (safe for strings)
        try:
            return eval(f'"{text}"')
        except:
            print("Error: Invalid escape sequence", file=sys.stderr)
            sys.exit(1)
    elif language in ["javascript", "js"]:
        # JavaScript unescape
        text = text.replace("\\n", "\n")
        text = text.replace("\\r", "\r")
        text = text.replace("\\t", "\t")
        text = text.replace('\\"', '"')
        text = text.replace("\\'", "'")
        text = text.replace("\\\\", "\\")
        return text
    elif language in ["sql"]:
        # SQL unescape (double single quotes to single)
        return text.replace("''", "'")
    else:
        print(f"Error: Unsupported language '{language}'", file=sys.stderr)
        sys.exit(1)


def handle_command(args):
    """Handle text conversion command."""
    operation = args.operation.lower()

    # Get input text
    if args.text:
        text = args.text
    elif args.file:
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        # Read from stdin
        text = sys.stdin.read()

    # Perform conversion
    if operation in ["url-encode", "urlencode", "url"]:
        result = url_encode(text)
    elif operation in ["url-decode", "urldecode"]:
        result = url_decode(text)
    elif operation in ["html-encode", "htmlencode"]:
        result = html_encode(text)
    elif operation in ["html-decode", "htmldecode"]:
        result = html_decode(text)
    elif operation in ["line-endings", "lineendings", "newline"]:
        if not args.target:
            print("Error: Target line ending format required", file=sys.stderr)
            sys.exit(1)
        result = convert_line_endings(text, args.target)
    elif operation in ["escape"]:
        if not args.target:
            print("Error: Target language required for escape", file=sys.stderr)
            sys.exit(1)
        result = escape_string(text, args.target)
    elif operation in ["unescape"]:
        if not args.target:
            print("Error: Source language required for unescape", file=sys.stderr)
            sys.exit(1)
        result = unescape_string(text, args.target)
    else:
        print(f"Error: Unsupported operation '{operation}'", file=sys.stderr)
        sys.exit(1)

    print(result)


def setup_parser(subparsers):
    """Setup text conversion subparser."""
    text_parser = subparsers.add_parser(
        "text",
        help="Convert text encodings and formats",
        description="Convert text between different encodings, escape formats, and line endings.",
    )
    text_parser.add_argument(
        "operation",
        type=str,
        help="Operation: url-encode, url-decode, html-encode, html-decode, line-endings, escape, unescape",
    )
    text_parser.add_argument(
        "text",
        type=str,
        nargs="?",
        help="Text to convert (or use --file or stdin)",
    )
    text_parser.add_argument(
        "--target",
        "-t",
        type=str,
        help="Target format (for line-endings, escape, unescape)",
    )
    text_parser.add_argument(
        "--file",
        "-f",
        type=str,
        help="Input file (instead of text argument)",
    )
    text_parser.set_defaults(func=handle_command)
