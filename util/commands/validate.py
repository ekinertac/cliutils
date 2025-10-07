import base64
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from typing import Optional

import tomli
import xmltodict
import yaml


def validate_json(content: str) -> tuple[bool, Optional[str]]:
    """Validate JSON syntax."""
    try:
        json.loads(content)
        return True, None
    except json.JSONDecodeError as e:
        return False, str(e)


def validate_yaml(content: str) -> tuple[bool, Optional[str]]:
    """Validate YAML syntax."""
    try:
        yaml.safe_load(content)
        return True, None
    except yaml.YAMLError as e:
        return False, str(e)


def validate_toml(content: str) -> tuple[bool, Optional[str]]:
    """Validate TOML syntax."""
    try:
        tomli.loads(content)
        return True, None
    except tomli.TOMLDecodeError as e:
        return False, str(e)


def validate_xml(content: str) -> tuple[bool, Optional[str]]:
    """Validate XML syntax."""
    try:
        xmltodict.parse(content)
        return True, None
    except Exception as e:
        return False, str(e)


def validate_html(content: str) -> tuple[bool, Optional[str]]:
    """Basic HTML validation (tag matching)."""
    try:
        # Simple validation: check for basic structure and matching tags
        # Note: This is basic validation, not a full HTML parser
        stack = []
        # Simplified regex to find tags
        tag_pattern = re.compile(r"<(/?)(\w+)[^>]*>")

        for match in tag_pattern.finditer(content):
            is_closing = match.group(1) == "/"
            tag_name = match.group(2).lower()

            # Skip self-closing tags
            if tag_name in [
                "br",
                "hr",
                "img",
                "input",
                "meta",
                "link",
                "area",
                "base",
                "col",
                "embed",
                "source",
                "track",
                "wbr",
            ]:
                continue

            if is_closing:
                if not stack or stack[-1] != tag_name:
                    return False, f"Mismatched closing tag: </{tag_name}>"
                stack.pop()
            else:
                stack.append(tag_name)

        if stack:
            return False, f"Unclosed tags: {', '.join(stack)}"

        return True, None
    except Exception as e:
        return False, str(e)


def validate_css(content: str) -> tuple[bool, Optional[str]]:
    """Basic CSS validation (brace matching)."""
    try:
        # Basic validation: check for matching braces
        brace_count = 0
        paren_count = 0
        bracket_count = 0

        for char in content:
            if char == "{":
                brace_count += 1
            elif char == "}":
                brace_count -= 1
                if brace_count < 0:
                    return False, "Unmatched closing brace }"
            elif char == "(":
                paren_count += 1
            elif char == ")":
                paren_count -= 1
                if paren_count < 0:
                    return False, "Unmatched closing parenthesis )"
            elif char == "[":
                bracket_count += 1
            elif char == "]":
                bracket_count -= 1
                if bracket_count < 0:
                    return False, "Unmatched closing bracket ]"

        if brace_count > 0:
            return False, "Unclosed braces"
        elif paren_count > 0:
            return False, "Unclosed parentheses"
        elif bracket_count > 0:
            return False, "Unclosed brackets"

        return True, None
    except Exception as e:
        return False, str(e)


def validate_email(email: str) -> tuple[bool, Optional[str]]:
    """Validate email address format."""
    # RFC 5322 compliant email regex (simplified)
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if re.match(pattern, email):
        return True, None
    else:
        return False, "Invalid email format"


def validate_url(url: str) -> tuple[bool, Optional[str]]:
    """Validate URL format."""
    # URL validation regex
    pattern = re.compile(
        r"^https?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain
        r"localhost|"  # localhost
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # or IP
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    if pattern.match(url):
        return True, None
    else:
        return False, "Invalid URL format"


def validate_ipv4(ip: str) -> tuple[bool, Optional[str]]:
    """Validate IPv4 address."""
    pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"
    match = re.match(pattern, ip)

    if not match:
        return False, "Invalid IPv4 format"

    # Check each octet is in range 0-255
    for octet in match.groups():
        if int(octet) > 255:
            return False, f"Octet {octet} exceeds 255"

    return True, None


def validate_ipv6(ip: str) -> tuple[bool, Optional[str]]:
    """Validate IPv6 address."""
    # Simplified IPv6 validation
    pattern = r"^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$"

    if re.match(pattern, ip):
        return True, None
    else:
        return False, "Invalid IPv6 format"


def validate_credit_card(number: str) -> tuple[bool, Optional[str]]:
    """Validate credit card number using Luhn algorithm."""
    # Remove spaces and hyphens
    number = number.replace(" ", "").replace("-", "")

    # Check if all characters are digits
    if not number.isdigit():
        return False, "Credit card number must contain only digits"

    # Check length (typically 13-19 digits)
    if len(number) < 13 or len(number) > 19:
        return False, "Credit card number must be 13-19 digits"

    # Luhn algorithm
    def luhn_checksum(card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10

    if luhn_checksum(number) == 0:
        return True, None
    else:
        return False, "Invalid credit card number (Luhn check failed)"


def validate_checksum(
    file_path: str, expected_hash: str, algorithm: str
) -> tuple[bool, Optional[str]]:
    """Validate file checksum."""
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"

    # Get hash algorithm
    algorithm = algorithm.lower()
    hash_algorithms = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha224": hashlib.sha224,
        "sha256": hashlib.sha256,
        "sha384": hashlib.sha384,
        "sha512": hashlib.sha512,
    }

    if algorithm not in hash_algorithms:
        return False, f"Unsupported hash algorithm: {algorithm}"

    try:
        hash_obj = hash_algorithms[algorithm]()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)

        actual_hash = hash_obj.hexdigest()
        expected_hash = expected_hash.lower()

        if actual_hash == expected_hash:
            return True, None
        else:
            return (
                False,
                f"Checksum mismatch: expected {expected_hash}, got {actual_hash}",
            )
    except Exception as e:
        return False, str(e)


def validate_uuid(uuid_str: str) -> tuple[bool, Optional[str]]:
    """Validate UUID format (v1, v3, v4, v5)."""
    # UUID regex pattern
    pattern = (
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    )

    uuid_str = uuid_str.lower()
    if re.match(pattern, uuid_str):
        # Detect version
        version = uuid_str[14]
        return True, f"Valid UUID v{version}"
    else:
        return False, "Invalid UUID format"


def validate_base64_string(text: str) -> tuple[bool, Optional[str]]:
    """Validate if string is valid base64."""
    try:
        # Remove whitespace
        text = text.strip()

        # Check if contains only valid base64 characters
        if not re.match(r"^[A-Za-z0-9+/]*={0,2}$", text):
            return False, "Contains invalid base64 characters"

        # Add padding if missing
        missing_padding = len(text) % 4
        if missing_padding:
            text += "=" * (4 - missing_padding)

        # Try to decode
        decoded = base64.b64decode(text, validate=True)

        # Re-encode to check if it matches (canonical check)
        reencoded = base64.b64encode(decoded).decode("ascii")

        # Allow for padding differences
        if text.rstrip("=") == reencoded.rstrip("="):
            return True, None
        else:
            return False, "Invalid base64 encoding"
    except Exception as e:
        return False, str(e)


def validate_iso8601_date(date_str: str) -> tuple[bool, Optional[str]]:
    """Validate ISO 8601 date/datetime format."""
    # Common ISO 8601 formats
    formats = [
        "%Y-%m-%d",  # 2023-12-31
        "%Y-%m-%dT%H:%M:%S",  # 2023-12-31T23:59:59
        "%Y-%m-%dT%H:%M:%SZ",  # 2023-12-31T23:59:59Z
        "%Y-%m-%dT%H:%M:%S.%f",  # 2023-12-31T23:59:59.123456
        "%Y-%m-%dT%H:%M:%S.%fZ",  # 2023-12-31T23:59:59.123456Z
    ]

    # Try timezone offset formats
    tz_pattern = r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?)[+-]\d{2}:\d{2}$"
    if re.match(tz_pattern, date_str):
        # Remove timezone offset for parsing
        date_part = re.match(tz_pattern, date_str).group(1)
        if "." in date_part:
            fmt = "%Y-%m-%dT%H:%M:%S.%f"
        else:
            fmt = "%Y-%m-%dT%H:%M:%S"
        try:
            datetime.strptime(date_part, fmt)
            return True, None
        except ValueError:
            pass

    for fmt in formats:
        try:
            datetime.strptime(date_str, fmt)
            return True, None
        except ValueError:
            continue

    return False, "Invalid ISO 8601 date format"


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """Validate password strength."""
    issues = []
    score = 0

    # Length check
    if len(password) < 8:
        issues.append("too short (minimum 8 characters)")
    elif len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1

    # Character variety checks
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

    if not has_lower:
        issues.append("no lowercase letters")
    else:
        score += 1

    if not has_upper:
        issues.append("no uppercase letters")
    else:
        score += 1

    if not has_digit:
        issues.append("no digits")
    else:
        score += 1

    if not has_special:
        issues.append("no special characters")
    else:
        score += 1

    # Common patterns to avoid
    common_patterns = [
        r"^password",
        r"12345",
        r"qwerty",
        r"abc123",
        r"^admin",
    ]

    for pattern in common_patterns:
        if re.search(pattern, password.lower()):
            issues.append("contains common pattern")
            score -= 1
            break

    # Determine strength
    if score < 3:
        strength = "weak"
    elif score < 5:
        strength = "moderate"
    elif score < 7:
        strength = "strong"
    else:
        strength = "very strong"

    if issues:
        return False, f"Password is {strength} ({', '.join(issues)})"
    else:
        return True, f"Password is {strength}"


def validate_regex_syntax(pattern: str) -> tuple[bool, Optional[str]]:
    """Validate regular expression syntax."""
    try:
        re.compile(pattern)
        return True, None
    except re.error as e:
        return False, f"Invalid regex: {str(e)}"


def validate_cron_expression(cron_expr: str) -> tuple[bool, Optional[str]]:
    """Validate cron expression format."""
    parts = cron_expr.strip().split()

    # Cron can have 5 or 6 fields (with optional seconds field)
    if len(parts) not in [5, 6]:
        return False, f"Expected 5 or 6 fields, got {len(parts)}"

    # Define validation patterns for each field
    # minute (0-59), hour (0-23), day of month (1-31), month (1-12), day of week (0-6)
    field_patterns = {
        0: (
            r"^(\*|([0-5]?[0-9])(,([0-5]?[0-9]))*|([0-5]?[0-9])-([0-5]?[0-9])|(\*/[0-9]+))$",
            "minute",
            0,
            59,
        ),
        1: (
            r"^(\*|(1?[0-9]|2[0-3])(,(1?[0-9]|2[0-3]))*|(1?[0-9]|2[0-3])-(1?[0-9]|2[0-3])|(\*/[0-9]+))$",
            "hour",
            0,
            23,
        ),
        2: (
            r"^(\*|([1-9]|[12][0-9]|3[01])(,([1-9]|[12][0-9]|3[01]))*|([1-9]|[12][0-9]|3[01])-([1-9]|[12][0-9]|3[01])|(\*/[0-9]+))$",
            "day",
            1,
            31,
        ),
        3: (
            r"^(\*|([1-9]|1[0-2])(,([1-9]|1[0-2]))*|([1-9]|1[0-2])-([1-9]|1[0-2])|(\*/[0-9]+))$",
            "month",
            1,
            12,
        ),
        4: (r"^(\*|[0-6](,[0-6])*|[0-6]-[0-6]|(\*/[0-9]+))$", "weekday", 0, 6),
    }

    # If 6 fields, first is seconds
    start_idx = 0 if len(parts) == 5 else 1

    # Validate seconds field if present
    if len(parts) == 6:
        seconds_pattern = r"^(\*|([0-5]?[0-9])(,([0-5]?[0-9]))*|([0-5]?[0-9])-([0-5]?[0-9])|(\*/[0-9]+))$"
        if not re.match(seconds_pattern, parts[0]):
            return False, "Invalid seconds field"

    # Validate each field
    for i, (pattern, name, min_val, max_val) in field_patterns.items():
        field_idx = i + start_idx
        field = parts[field_idx]

        # Basic pattern check
        if not re.match(pattern, field):
            return False, f"Invalid {name} field: {field}"

    return True, None


def handle_syntax_validation(args):
    """Handle syntax validation commands."""
    format_type = args.format_type

    # Get content - auto-detect file vs direct content
    if args.input:
        # Check if input is a file path
        if os.path.exists(args.input) and os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            # Treat as direct content
            content = args.input
    else:
        # Read from stdin
        content = sys.stdin.read()

    # Validate based on format
    validators = {
        "json": validate_json,
        "yaml": validate_yaml,
        "yml": validate_yaml,
        "toml": validate_toml,
        "xml": validate_xml,
        "html": validate_html,
        "css": validate_css,
    }

    if format_type not in validators:
        print(f"Error: Unsupported format '{format_type}'", file=sys.stderr)
        sys.exit(1)

    is_valid, error_msg = validators[format_type](content)

    if is_valid:
        print(f"✓ Valid {format_type.upper()}")
        sys.exit(0)
    else:
        print(f"✗ Invalid {format_type.upper()}: {error_msg}", file=sys.stderr)
        sys.exit(1)


def handle_email_validation(args):
    """Handle email validation."""
    is_valid, error_msg = validate_email(args.email)

    if is_valid:
        print(f"✓ Valid email: {args.email}")
        sys.exit(0)
    else:
        print(f"✗ Invalid email: {error_msg}", file=sys.stderr)
        sys.exit(1)


def handle_url_validation(args):
    """Handle URL validation."""
    is_valid, error_msg = validate_url(args.url)

    if is_valid:
        print(f"✓ Valid URL: {args.url}")
        sys.exit(0)
    else:
        print(f"✗ Invalid URL: {error_msg}", file=sys.stderr)
        sys.exit(1)


def handle_ip_validation(args):
    """Handle IP address validation."""
    ip = args.ip
    version = args.version

    if version == "4" or version == "auto":
        is_valid, error_msg = validate_ipv4(ip)
        if is_valid:
            print(f"✓ Valid IPv4: {ip}")
            sys.exit(0)
        elif version == "4":
            print(f"✗ Invalid IPv4: {error_msg}", file=sys.stderr)
            sys.exit(1)

    if version == "6" or version == "auto":
        is_valid, error_msg = validate_ipv6(ip)
        if is_valid:
            print(f"✓ Valid IPv6: {ip}")
            sys.exit(0)
        elif version == "6":
            print(f"✗ Invalid IPv6: {error_msg}", file=sys.stderr)
            sys.exit(1)

    if version == "auto":
        print("✗ Invalid IP address", file=sys.stderr)
        sys.exit(1)


def handle_credit_card_validation(args):
    """Handle credit card validation."""
    is_valid, error_msg = validate_credit_card(args.number)

    if is_valid:
        print("✓ Valid credit card number")
        sys.exit(0)
    else:
        print(f"✗ Invalid credit card: {error_msg}", file=sys.stderr)
        sys.exit(1)


def handle_checksum_validation(args):
    """Handle file checksum validation."""
    is_valid, error_msg = validate_checksum(args.file, args.checksum, args.algorithm)

    if is_valid:
        print(f"✓ Checksum verified: {args.file}")
        sys.exit(0)
    else:
        print(f"✗ Checksum validation failed: {error_msg}", file=sys.stderr)
        sys.exit(1)


def handle_uuid_validation(args):
    """Handle UUID validation."""
    is_valid, msg = validate_uuid(args.uuid)

    if is_valid:
        print(f"✓ {msg}: {args.uuid}")
        sys.exit(0)
    else:
        print(f"✗ Invalid UUID: {msg}", file=sys.stderr)
        sys.exit(1)


def handle_base64_validation(args):
    """Handle base64 validation."""
    is_valid, error_msg = validate_base64_string(args.text)

    if is_valid:
        print("✓ Valid base64")
        sys.exit(0)
    else:
        print(f"✗ Invalid base64: {error_msg}", file=sys.stderr)
        sys.exit(1)


def handle_date_validation(args):
    """Handle ISO 8601 date validation."""
    is_valid, error_msg = validate_iso8601_date(args.date)

    if is_valid:
        print(f"✓ Valid ISO 8601 date: {args.date}")
        sys.exit(0)
    else:
        print(f"✗ Invalid date: {error_msg}", file=sys.stderr)
        sys.exit(1)


def handle_password_validation(args):
    """Handle password strength validation."""
    is_valid, msg = validate_password_strength(args.password)

    if is_valid:
        print(f"✓ {msg}")
        sys.exit(0)
    else:
        print(f"✗ {msg}", file=sys.stderr)
        sys.exit(1)


def handle_regex_validation(args):
    """Handle regex syntax validation."""
    is_valid, error_msg = validate_regex_syntax(args.pattern)

    if is_valid:
        print("✓ Valid regex pattern")
        sys.exit(0)
    else:
        print(f"✗ {error_msg}", file=sys.stderr)
        sys.exit(1)


def handle_cron_validation(args):
    """Handle cron expression validation."""
    is_valid, error_msg = validate_cron_expression(args.expression)

    if is_valid:
        print("✓ Valid cron expression")
        sys.exit(0)
    else:
        print(f"✗ Invalid cron: {error_msg}", file=sys.stderr)
        sys.exit(1)


def setup_parser(subparsers):
    """Setup the validate parser."""
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate syntax, formats, and checksums",
        description="Validate JSON/YAML/TOML/XML/HTML/CSS syntax, email addresses, URLs, IP addresses, credit cards, file checksums, UUIDs, base64, dates, passwords, regex, and cron expressions.",
    )
    validate_subparsers = validate_parser.add_subparsers(
        dest="validate_type", required=True, help="Type of validation"
    )

    # Syntax validation
    syntax_parser = validate_subparsers.add_parser(
        "syntax",
        help="Validate file syntax (JSON, YAML, TOML, XML, HTML, CSS)",
    )
    syntax_parser.add_argument(
        "format_type",
        choices=["json", "yaml", "yml", "toml", "xml", "html", "css"],
        help="Format to validate",
    )
    syntax_parser.add_argument(
        "input",
        nargs="?",
        help="File path or content to validate (auto-detected, or use stdin)",
    )
    syntax_parser.set_defaults(func=handle_syntax_validation)

    # Email validation
    email_parser = validate_subparsers.add_parser(
        "email",
        help="Validate email address",
    )
    email_parser.add_argument("email", help="Email address to validate")
    email_parser.set_defaults(func=handle_email_validation)

    # URL validation
    url_parser = validate_subparsers.add_parser(
        "url",
        help="Validate URL",
    )
    url_parser.add_argument("url", help="URL to validate")
    url_parser.set_defaults(func=handle_url_validation)

    # IP validation
    ip_parser = validate_subparsers.add_parser(
        "ip",
        help="Validate IP address (IPv4 or IPv6)",
    )
    ip_parser.add_argument("ip", help="IP address to validate")
    ip_parser.add_argument(
        "--version",
        "-v",
        choices=["4", "6", "auto"],
        default="auto",
        help="IP version (default: auto-detect)",
    )
    ip_parser.set_defaults(func=handle_ip_validation)

    # Credit card validation
    card_parser = validate_subparsers.add_parser(
        "card",
        aliases=["credit-card", "cc"],
        help="Validate credit card number (Luhn algorithm)",
    )
    card_parser.add_argument("number", help="Credit card number to validate")
    card_parser.set_defaults(func=handle_credit_card_validation)

    # Checksum validation
    checksum_parser = validate_subparsers.add_parser(
        "checksum",
        aliases=["hash"],
        help="Validate file checksum",
    )
    checksum_parser.add_argument("file", help="File to validate")
    checksum_parser.add_argument("checksum", help="Expected checksum")
    checksum_parser.add_argument(
        "--algorithm",
        "-a",
        choices=["md5", "sha1", "sha224", "sha256", "sha384", "sha512"],
        default="sha256",
        help="Hash algorithm (default: sha256)",
    )
    checksum_parser.set_defaults(func=handle_checksum_validation)

    # UUID validation
    uuid_parser = validate_subparsers.add_parser(
        "uuid",
        help="Validate UUID format",
    )
    uuid_parser.add_argument("uuid", help="UUID to validate")
    uuid_parser.set_defaults(func=handle_uuid_validation)

    # Base64 validation
    base64_parser = validate_subparsers.add_parser(
        "base64",
        aliases=["b64"],
        help="Validate base64 encoding",
    )
    base64_parser.add_argument("text", help="Base64 string to validate")
    base64_parser.set_defaults(func=handle_base64_validation)

    # Date validation
    date_parser = validate_subparsers.add_parser(
        "date",
        aliases=["iso8601"],
        help="Validate ISO 8601 date format",
    )
    date_parser.add_argument("date", help="Date string to validate")
    date_parser.set_defaults(func=handle_date_validation)

    # Password strength validation
    password_parser = validate_subparsers.add_parser(
        "password",
        aliases=["pwd", "pass"],
        help="Check password strength",
    )
    password_parser.add_argument("password", help="Password to check")
    password_parser.set_defaults(func=handle_password_validation)

    # Regex syntax validation
    regex_parser = validate_subparsers.add_parser(
        "regex",
        aliases=["regexp"],
        help="Validate regular expression syntax",
    )
    regex_parser.add_argument("pattern", help="Regex pattern to validate")
    regex_parser.set_defaults(func=handle_regex_validation)

    # Cron expression validation
    cron_parser = validate_subparsers.add_parser(
        "cron",
        help="Validate cron expression",
    )
    cron_parser.add_argument("expression", help="Cron expression to validate")
    cron_parser.set_defaults(func=handle_cron_validation)
