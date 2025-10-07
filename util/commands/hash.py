import hashlib
import sys


def hash_command(args):
    """Generate cryptographic hash digests."""
    text = args.text

    # Get the hash algorithm
    hash_type = args.hash_type

    try:
        # Create hash object based on type
        if hash_type == "md5":
            hash_obj = hashlib.md5()
        elif hash_type == "sha1":
            hash_obj = hashlib.sha1()
        elif hash_type == "sha224":
            hash_obj = hashlib.sha224()
        elif hash_type == "sha256":
            hash_obj = hashlib.sha256()
        elif hash_type == "sha384":
            hash_obj = hashlib.sha384()
        elif hash_type == "sha512":
            hash_obj = hashlib.sha512()
        else:
            print(f"Error: Unsupported hash type '{hash_type}'", file=sys.stderr)
            sys.exit(1)

        # Update hash with text (encoded as bytes)
        hash_obj.update(text.encode("utf-8"))

        # Print the hexadecimal digest
        print(hash_obj.hexdigest())

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def setup_parser(subparsers):
    hash_parser = subparsers.add_parser(
        "hash",
        help="Generate cryptographic hash digests",
        description="Generate cryptographic hash digests (MD5, SHA1, SHA224, SHA256, SHA384, SHA512).",
    )
    hash_subparsers = hash_parser.add_subparsers(
        dest="hash_type", required=True, help="Type of hash to generate"
    )

    # MD5 subcommand
    md5_parser = hash_subparsers.add_parser(
        "md5", help="Generate MD5 hash", description="Generate MD5 hash digest."
    )
    md5_parser.add_argument("text", type=str, help="Text to hash")
    md5_parser.set_defaults(func=hash_command)

    # SHA1 subcommand
    sha1_parser = hash_subparsers.add_parser(
        "sha1", help="Generate SHA1 hash", description="Generate SHA1 hash digest."
    )
    sha1_parser.add_argument("text", type=str, help="Text to hash")
    sha1_parser.set_defaults(func=hash_command)

    # SHA224 subcommand
    sha224_parser = hash_subparsers.add_parser(
        "sha224",
        help="Generate SHA224 hash",
        description="Generate SHA224 hash digest.",
    )
    sha224_parser.add_argument("text", type=str, help="Text to hash")
    sha224_parser.set_defaults(func=hash_command)

    # SHA256 subcommand
    sha256_parser = hash_subparsers.add_parser(
        "sha256",
        help="Generate SHA256 hash",
        description="Generate SHA256 hash digest.",
    )
    sha256_parser.add_argument("text", type=str, help="Text to hash")
    sha256_parser.set_defaults(func=hash_command)

    # SHA384 subcommand
    sha384_parser = hash_subparsers.add_parser(
        "sha384",
        help="Generate SHA384 hash",
        description="Generate SHA384 hash digest.",
    )
    sha384_parser.add_argument("text", type=str, help="Text to hash")
    sha384_parser.set_defaults(func=hash_command)

    # SHA512 subcommand
    sha512_parser = hash_subparsers.add_parser(
        "sha512",
        help="Generate SHA512 hash",
        description="Generate SHA512 hash digest.",
    )
    sha512_parser.add_argument("text", type=str, help="Text to hash")
    sha512_parser.set_defaults(func=hash_command)
