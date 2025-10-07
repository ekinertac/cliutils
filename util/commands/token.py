import secrets
import string
import sys


def token_command(args):
    """Generate secure tokens and secrets."""
    token_type = args.token_type

    try:
        if token_type == "hex":
            # Generate random hexadecimal token
            token = secrets.token_hex(args.bytes)
            print(token)

        elif token_type == "urlsafe":
            # Generate URL-safe token
            token = secrets.token_urlsafe(args.bytes)
            print(token)

        elif token_type == "bytes":
            # Generate random bytes as hex string
            token = secrets.token_bytes(args.bytes).hex()
            print(token)

        elif token_type in ["password", "pwd", "pass"]:
            # Generate secure random password
            length = args.length
            if length < 1:
                print("Error: Password length must be at least 1", file=sys.stderr)
                sys.exit(1)

            # Character set for password
            alphabet = string.ascii_letters + string.digits
            if args.special:
                alphabet += string.punctuation

            password = "".join(secrets.choice(alphabet) for _ in range(length))
            print(password)

        else:
            print(f"Error: Unsupported token type '{token_type}'", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def setup_parser(subparsers):
    token_parser = subparsers.add_parser(
        "token",
        help="Generate secure tokens and secrets",
        description="Generate cryptographically strong random tokens, secrets, and passwords.",
    )
    token_subparsers = token_parser.add_subparsers(
        dest="token_type", required=True, help="Type of token to generate"
    )

    # Hex token subcommand
    hex_parser = token_subparsers.add_parser(
        "hex",
        help="Generate random hexadecimal token",
        description="Generate random hexadecimal token.",
    )
    hex_parser.add_argument(
        "--bytes",
        type=int,
        default=32,
        help="Number of bytes for token (default: 32)",
    )
    hex_parser.set_defaults(func=token_command)

    # URL-safe token subcommand
    urlsafe_parser = token_subparsers.add_parser(
        "urlsafe",
        help="Generate URL-safe token",
        description="Generate URL-safe token (Base64 encoded).",
    )
    urlsafe_parser.add_argument(
        "--bytes",
        type=int,
        default=32,
        help="Number of bytes for token (default: 32)",
    )
    urlsafe_parser.set_defaults(func=token_command)

    # Bytes token subcommand
    bytes_parser = token_subparsers.add_parser(
        "bytes",
        help="Generate random bytes token",
        description="Generate random bytes token (displayed as hex).",
    )
    bytes_parser.add_argument(
        "--bytes",
        type=int,
        default=32,
        help="Number of bytes for token (default: 32)",
    )
    bytes_parser.set_defaults(func=token_command)

    # Password subcommand
    password_parser = token_subparsers.add_parser(
        "password",
        aliases=["pwd", "pass"],
        help="Generate secure random password",
        description="Generate cryptographically strong random password.",
    )
    password_parser.add_argument(
        "--length",
        type=int,
        default=16,
        help="Length of password (default: 16)",
    )
    password_parser.add_argument(
        "--special",
        action="store_true",
        help="Include special characters in password",
    )
    password_parser.set_defaults(func=token_command)
