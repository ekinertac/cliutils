import random
import re
import sys


def to_lower(text):
    """Convert text to lowercase."""
    return text.lower()


def to_upper(text):
    """Convert text to UPPERCASE."""
    return text.upper()


def to_camel(text):
    """Convert text to camelCase."""
    # Split on spaces, hyphens, underscores
    words = re.split(r"[\s\-_]+", text.strip())
    if not words:
        return ""
    # First word lowercase, rest title case
    result = words[0].lower()
    for word in words[1:]:
        if word:
            result += word.capitalize()
    return result


def to_pascal(text):
    """Convert text to PascalCase."""
    # Split on spaces, hyphens, underscores
    words = re.split(r"[\s\-_]+", text.strip())
    return "".join(word.capitalize() for word in words if word)


def to_snake(text):
    """Convert text to snake_case."""
    # Handle camelCase/PascalCase - insert underscore before capital letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    # Replace spaces and hyphens with underscores
    text = re.sub(r"[\s\-]+", "_", text)
    # Convert to lowercase
    return text.lower()


def to_constant(text):
    """Convert text to CONSTANT_CASE."""
    return to_snake(text).upper()


def to_kebab(text):
    """Convert text to kebab-case."""
    # Handle camelCase/PascalCase - insert hyphen before capital letters
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", text)
    # Replace spaces and underscores with hyphens
    text = re.sub(r"[\s_]+", "-", text)
    # Convert to lowercase
    return text.lower()


def to_header(text):
    """Convert text to Header-Case."""
    # Split on spaces, hyphens, underscores
    words = re.split(r"[\s\-_]+", text.strip())
    return "-".join(word.capitalize() for word in words if word)


def to_title(text):
    """Convert text to Title Case."""
    # Split on spaces, hyphens, underscores but keep the separators
    words = re.split(r"(\s+|-|_)", text.strip())
    result = []
    for i, word in enumerate(words):
        if word and not re.match(r"[\s\-_]+", word):
            result.append(word.capitalize())
        else:
            result.append(word)
    return "".join(result)


def to_sentence(text):
    """Convert text to Sentence case."""
    if not text:
        return ""
    # First character uppercase, rest lowercase
    return text[0].upper() + text[1:].lower()


def case_command(args):
    """Convert text case formats."""
    case_type = args.case_type
    text = args.text

    try:
        if case_type == "lower":
            result = to_lower(text)
        elif case_type == "upper":
            result = to_upper(text)
        elif case_type == "camel":
            result = to_camel(text)
        elif case_type == "pascal":
            result = to_pascal(text)
        elif case_type == "snake":
            result = to_snake(text)
        elif case_type == "constant":
            result = to_constant(text)
        elif case_type == "kebab":
            result = to_kebab(text)
        elif case_type == "header":
            result = to_header(text)
        elif case_type == "title":
            result = to_title(text)
        elif case_type == "sentence":
            result = to_sentence(text)
        else:
            print(f"Error: Unsupported case type '{case_type}'", file=sys.stderr)
            sys.exit(1)

        print(result)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def setup_parser(subparsers):
    case_parser = subparsers.add_parser(
        "case",
        help="Convert text case formats",
        description="Convert text between different case formats (camelCase, snake_case, etc.).",
    )
    case_subparsers = case_parser.add_subparsers(
        dest="case_type", required=True, help="Type of case to convert to"
    )

    # Lower case subcommand
    lower_parser = case_subparsers.add_parser(
        "lower", help="Convert to lowercase", description="Convert text to lowercase."
    )
    lower_parser.add_argument("text", type=str, help="Text to convert")
    lower_parser.set_defaults(func=case_command)

    # Upper case subcommand
    upper_parser = case_subparsers.add_parser(
        "upper",
        help="Convert to UPPERCASE",
        description="Convert text to UPPERCASE.",
    )
    upper_parser.add_argument("text", type=str, help="Text to convert")
    upper_parser.set_defaults(func=case_command)

    # Camel case subcommand
    camel_parser = case_subparsers.add_parser(
        "camel",
        help="Convert to camelCase",
        description="Convert text to camelCase.",
    )
    camel_parser.add_argument("text", type=str, help="Text to convert")
    camel_parser.set_defaults(func=case_command)

    # Pascal case subcommand
    pascal_parser = case_subparsers.add_parser(
        "pascal",
        help="Convert to PascalCase",
        description="Convert text to PascalCase.",
    )
    pascal_parser.add_argument("text", type=str, help="Text to convert")
    pascal_parser.set_defaults(func=case_command)

    # Snake case subcommand
    snake_parser = case_subparsers.add_parser(
        "snake",
        help="Convert to snake_case",
        description="Convert text to snake_case.",
    )
    snake_parser.add_argument("text", type=str, help="Text to convert")
    snake_parser.set_defaults(func=case_command)

    # Constant case subcommand
    constant_parser = case_subparsers.add_parser(
        "constant",
        help="Convert to CONSTANT_CASE",
        description="Convert text to CONSTANT_CASE.",
    )
    constant_parser.add_argument("text", type=str, help="Text to convert")
    constant_parser.set_defaults(func=case_command)

    # Kebab case subcommand
    kebab_parser = case_subparsers.add_parser(
        "kebab",
        help="Convert to kebab-case",
        description="Convert text to kebab-case.",
    )
    kebab_parser.add_argument("text", type=str, help="Text to convert")
    kebab_parser.set_defaults(func=case_command)

    # Header case subcommand
    header_parser = case_subparsers.add_parser(
        "header",
        help="Convert to Header-Case",
        description="Convert text to Header-Case.",
    )
    header_parser.add_argument("text", type=str, help="Text to convert")
    header_parser.set_defaults(func=case_command)

    # Title case subcommand
    title_parser = case_subparsers.add_parser(
        "title",
        help="Convert to Title Case",
        description="Convert text to Title Case.",
    )
    title_parser.add_argument("text", type=str, help="Text to convert")
    title_parser.set_defaults(func=case_command)

    # Sentence case subcommand
    sentence_parser = case_subparsers.add_parser(
        "sentence",
        help="Convert to Sentence case",
        description="Convert text to Sentence case.",
    )
    sentence_parser.add_argument("text", type=str, help="Text to convert")
    sentence_parser.set_defaults(func=case_command)
