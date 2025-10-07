import random
import string
import sys


def random_command(args):
    """Generate random data."""
    random_type = args.random_type

    try:
        if random_type in ["int", "integer"]:
            # Generate random integer
            min_val = args.min
            max_val = args.max

            if min_val > max_val:
                print(
                    f"Error: min value ({min_val}) cannot be greater than max value ({max_val})",
                    file=sys.stderr,
                )
                sys.exit(1)

            result = random.randint(min_val, max_val)
            print(result)

        elif random_type == "float":
            # Generate random float
            min_val = args.min
            max_val = args.max

            if min_val > max_val:
                print(
                    f"Error: min value ({min_val}) cannot be greater than max value ({max_val})",
                    file=sys.stderr,
                )
                sys.exit(1)

            result = random.uniform(min_val, max_val)
            print(result)

        elif random_type in ["string", "str"]:
            # Generate random string
            length = args.length
            if length < 1:
                print("Error: String length must be at least 1", file=sys.stderr)
                sys.exit(1)

            # Build character set based on flags
            charset = ""
            if args.letters or (
                not args.letters and not args.digits and not args.punctuation
            ):
                charset += string.ascii_letters
            if args.digits or (
                not args.letters and not args.digits and not args.punctuation
            ):
                charset += string.digits
            if args.punctuation:
                charset += string.punctuation
            if args.lowercase:
                charset = string.ascii_lowercase
                if args.digits:
                    charset += string.digits
            if args.uppercase:
                charset = string.ascii_uppercase
                if args.digits:
                    charset += string.digits

            if not charset:
                charset = string.ascii_letters + string.digits

            result = "".join(random.choice(charset) for _ in range(length))
            print(result)

        elif random_type == "choice":
            # Pick random item from choices
            choices = args.choices
            if not choices:
                print("Error: No choices provided", file=sys.stderr)
                sys.exit(1)

            result = random.choice(choices)
            print(result)

        elif random_type == "shuffle":
            # Shuffle items
            items = args.items
            if not items:
                print("Error: No items provided", file=sys.stderr)
                sys.exit(1)

            result = items.copy()
            random.shuffle(result)
            print(" ".join(result))

        else:
            print(f"Error: Unsupported random type '{random_type}'", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def setup_parser(subparsers):
    random_parser = subparsers.add_parser(
        "random",
        help="Generate random data",
        description="Generate random integers, floats, strings, and more.",
    )
    random_subparsers = random_parser.add_subparsers(
        dest="random_type", required=True, help="Type of random data to generate"
    )

    # Integer subcommand
    int_parser = random_subparsers.add_parser(
        "int",
        aliases=["integer"],
        help="Generate random integer",
        description="Generate random integer within range.",
    )
    int_parser.add_argument(
        "--min", type=int, default=0, help="Minimum value (default: 0)"
    )
    int_parser.add_argument(
        "--max", type=int, default=100, help="Maximum value (default: 100)"
    )
    int_parser.set_defaults(func=random_command)

    # Float subcommand
    float_parser = random_subparsers.add_parser(
        "float",
        help="Generate random float",
        description="Generate random floating-point number within range.",
    )
    float_parser.add_argument(
        "--min", type=float, default=0.0, help="Minimum value (default: 0.0)"
    )
    float_parser.add_argument(
        "--max", type=float, default=1.0, help="Maximum value (default: 1.0)"
    )
    float_parser.set_defaults(func=random_command)

    # String subcommand
    string_parser = random_subparsers.add_parser(
        "string",
        aliases=["str"],
        help="Generate random string",
        description="Generate random string with specified characters.",
    )
    string_parser.add_argument(
        "--length", type=int, default=10, help="Length of string (default: 10)"
    )
    string_parser.add_argument(
        "--letters", action="store_true", help="Include letters (a-zA-Z)"
    )
    string_parser.add_argument(
        "--digits", action="store_true", help="Include digits (0-9)"
    )
    string_parser.add_argument(
        "--punctuation", action="store_true", help="Include punctuation characters"
    )
    string_parser.add_argument(
        "--lowercase", action="store_true", help="Only lowercase letters"
    )
    string_parser.add_argument(
        "--uppercase", action="store_true", help="Only uppercase letters"
    )
    string_parser.set_defaults(func=random_command)

    # Choice subcommand
    choice_parser = random_subparsers.add_parser(
        "choice",
        help="Pick random item from list",
        description="Pick a random item from provided choices.",
    )
    choice_parser.add_argument(
        "choices", nargs="+", help="List of choices to pick from"
    )
    choice_parser.set_defaults(func=random_command)

    # Shuffle subcommand
    shuffle_parser = random_subparsers.add_parser(
        "shuffle",
        help="Shuffle items randomly",
        description="Shuffle items in random order.",
    )
    shuffle_parser.add_argument("items", nargs="+", help="List of items to shuffle")
    shuffle_parser.set_defaults(func=random_command)
