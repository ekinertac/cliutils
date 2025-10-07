import base64
import html
import sys
import urllib.parse


def encode_url(text: str) -> str:
    """URL encode text."""
    return urllib.parse.quote(text)


def decode_url(text: str) -> str:
    """URL decode text."""
    return urllib.parse.unquote(text)


def encode_html(text: str) -> str:
    """Encode HTML entities."""
    return html.escape(text)


def decode_html(text: str) -> str:
    """Decode HTML entities."""
    return html.unescape(text)


def encode_unicode_escape(text: str) -> str:
    """Encode text to Unicode escape sequences."""
    return text.encode("unicode_escape").decode("ascii")


def decode_unicode_escape(text: str) -> str:
    """Decode Unicode escape sequences."""
    return text.encode("ascii").decode("unicode_escape")


def encode_hex(text: str) -> str:
    """Encode text to hexadecimal."""
    return text.encode("utf-8").hex()


def decode_hex(text: str) -> str:
    """Decode hexadecimal to text."""
    return bytes.fromhex(text).decode("utf-8")


def encode_base64(text: str) -> str:
    """Encode text to base64."""
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def decode_base64(text: str) -> str:
    """Decode base64 to text."""
    return base64.b64decode(text).decode("utf-8")


def encode_base32(text: str) -> str:
    """Encode text to base32."""
    return base64.b32encode(text.encode("utf-8")).decode("ascii")


def decode_base32(text: str) -> str:
    """Decode base32 to text."""
    return base64.b32decode(text).decode("utf-8")


def encode_binary(text: str) -> str:
    """Encode text to binary."""
    return " ".join(format(ord(char), "08b") for char in text)


def decode_binary(text: str) -> str:
    """Decode binary to text."""
    binary_values = text.replace(" ", "")
    chars = []
    for i in range(0, len(binary_values), 8):
        byte = binary_values[i : i + 8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return "".join(chars)


def encode_rot13(text: str) -> str:
    """Encode text using ROT13."""
    result = []
    for char in text:
        if "a" <= char <= "z":
            result.append(chr((ord(char) - ord("a") + 13) % 26 + ord("a")))
        elif "A" <= char <= "Z":
            result.append(chr((ord(char) - ord("A") + 13) % 26 + ord("A")))
        else:
            result.append(char)
    return "".join(result)


# ROT13 decode is the same as encode
decode_rot13 = encode_rot13


# Morse code dictionary
MORSE_CODE = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    "'": ".----.",
    "!": "-.-.--",
    "/": "-..-.",
    "(": "-.--.",
    ")": "-.--.-",
    "&": ".-...",
    ":": "---...",
    ";": "-.-.-.",
    "=": "-...-",
    "+": ".-.-.",
    "-": "-....-",
    "_": "..--.-",
    '"': ".-..-.",
    "$": "...-..-",
    "@": ".--.-.",
    " ": "/",
}

MORSE_CODE_REVERSE = {v: k for k, v in MORSE_CODE.items()}


def encode_morse(text: str) -> str:
    """Encode text to Morse code."""
    return " ".join(MORSE_CODE.get(char.upper(), "") for char in text)


def decode_morse(text: str) -> str:
    """Decode Morse code to text."""
    words = text.split(" / ")
    result = []
    for word in words:
        chars = word.split()
        decoded_word = "".join(MORSE_CODE_REVERSE.get(char, "") for char in chars)
        result.append(decoded_word)
    return " ".join(result)


def hex_dump(text: str, width: int = 16) -> str:
    """Create a hex dump of text."""
    data = text.encode("utf-8")
    lines = []
    for i in range(0, len(data), width):
        chunk = data[i : i + width]
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        # Pad hex part if needed
        hex_part = hex_part.ljust(width * 3 - 1)
        # ASCII representation
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        lines.append(f"{i:08x}  {hex_part}  |{ascii_part}|")
    return "\n".join(lines)


def handle_url_command(args):
    """Handle URL encoding/decoding."""
    if args.operation == "encode":
        result = encode_url(args.text)
    else:  # decode
        result = decode_url(args.text)
    print(result)


def handle_html_command(args):
    """Handle HTML entity encoding/decoding."""
    if args.operation == "encode":
        result = encode_html(args.text)
    else:  # decode
        result = decode_html(args.text)
    print(result)


def handle_unicode_command(args):
    """Handle Unicode escape encoding/decoding."""
    try:
        if args.operation == "encode":
            result = encode_unicode_escape(args.text)
        else:  # decode
            result = decode_unicode_escape(args.text)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_hex_command(args):
    """Handle hex encoding/decoding."""
    try:
        if args.operation == "encode":
            result = encode_hex(args.text)
        else:  # decode
            result = decode_hex(args.text)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_hexdump_command(args):
    """Handle hex dump."""
    result = hex_dump(args.text, width=args.width)
    print(result)


def handle_base64_command(args):
    """Handle base64 encoding/decoding."""
    try:
        if args.operation == "encode":
            result = encode_base64(args.text)
        else:  # decode
            result = decode_base64(args.text)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_base32_command(args):
    """Handle base32 encoding/decoding."""
    try:
        if args.operation == "encode":
            result = encode_base32(args.text)
        else:  # decode
            result = decode_base32(args.text)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_binary_command(args):
    """Handle binary encoding/decoding."""
    try:
        if args.operation == "encode":
            result = encode_binary(args.text)
        else:  # decode
            result = decode_binary(args.text)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_rot13_command(args):
    """Handle ROT13 encoding/decoding."""
    result = encode_rot13(args.text)
    print(result)


def handle_morse_command(args):
    """Handle Morse code encoding/decoding."""
    try:
        if args.operation == "encode":
            result = encode_morse(args.text)
        else:  # decode
            result = decode_morse(args.text)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def setup_parser(subparsers):
    """Setup the encode parser."""
    encode_parser = subparsers.add_parser(
        "encode",
        help="Encode/decode text in various formats",
        description="Encode and decode text using URL, HTML, base64, hex, morse code, and more.",
    )
    encode_subparsers = encode_parser.add_subparsers(
        dest="encode_type", required=True, help="Type of encoding"
    )

    # URL encoding
    url_parser = encode_subparsers.add_parser(
        "url", help="URL encode/decode (percent encoding)"
    )
    url_parser.add_argument(
        "operation", choices=["encode", "decode"], help="Operation to perform"
    )
    url_parser.add_argument("text", help="Text to encode/decode")
    url_parser.set_defaults(func=handle_url_command)

    # HTML encoding
    html_parser = encode_subparsers.add_parser("html", help="HTML entity encode/decode")
    html_parser.add_argument(
        "operation", choices=["encode", "decode"], help="Operation to perform"
    )
    html_parser.add_argument("text", help="Text to encode/decode")
    html_parser.set_defaults(func=handle_html_command)

    # Unicode escape
    unicode_parser = encode_subparsers.add_parser(
        "unicode", aliases=["uni"], help="Unicode escape sequences"
    )
    unicode_parser.add_argument(
        "operation", choices=["encode", "decode"], help="Operation to perform"
    )
    unicode_parser.add_argument("text", help="Text to encode/decode")
    unicode_parser.set_defaults(func=handle_unicode_command)

    # Hex encoding
    hex_parser = encode_subparsers.add_parser("hex", help="Hexadecimal encode/decode")
    hex_parser.add_argument(
        "operation", choices=["encode", "decode"], help="Operation to perform"
    )
    hex_parser.add_argument("text", help="Text to encode/decode")
    hex_parser.set_defaults(func=handle_hex_command)

    # Hex dump
    hexdump_parser = encode_subparsers.add_parser(
        "hexdump", aliases=["dump"], help="Create hex dump"
    )
    hexdump_parser.add_argument("text", help="Text to dump")
    hexdump_parser.add_argument(
        "--width", "-w", type=int, default=16, help="Bytes per line (default: 16)"
    )
    hexdump_parser.set_defaults(func=handle_hexdump_command)

    # Base64
    base64_parser = encode_subparsers.add_parser(
        "base64", aliases=["b64"], help="Base64 encode/decode"
    )
    base64_parser.add_argument(
        "operation", choices=["encode", "decode"], help="Operation to perform"
    )
    base64_parser.add_argument("text", help="Text to encode/decode")
    base64_parser.set_defaults(func=handle_base64_command)

    # Base32
    base32_parser = encode_subparsers.add_parser(
        "base32", aliases=["b32"], help="Base32 encode/decode"
    )
    base32_parser.add_argument(
        "operation", choices=["encode", "decode"], help="Operation to perform"
    )
    base32_parser.add_argument("text", help="Text to encode/decode")
    base32_parser.set_defaults(func=handle_base32_command)

    # Binary
    binary_parser = encode_subparsers.add_parser(
        "binary", aliases=["bin"], help="Binary encode/decode"
    )
    binary_parser.add_argument(
        "operation", choices=["encode", "decode"], help="Operation to perform"
    )
    binary_parser.add_argument("text", help="Text to encode/decode")
    binary_parser.set_defaults(func=handle_binary_command)

    # ROT13
    rot13_parser = encode_subparsers.add_parser(
        "rot13", help="ROT13 encode/decode (Caesar cipher)"
    )
    rot13_parser.add_argument("text", help="Text to encode/decode")
    rot13_parser.set_defaults(func=handle_rot13_command)

    # Morse code
    morse_parser = encode_subparsers.add_parser(
        "morse", help="Morse code encode/decode"
    )
    morse_parser.add_argument(
        "operation", choices=["encode", "decode"], help="Operation to perform"
    )
    morse_parser.add_argument("text", help="Text to encode/decode")
    morse_parser.set_defaults(func=handle_morse_command)
