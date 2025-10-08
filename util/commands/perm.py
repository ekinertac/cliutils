import sys


def octal_to_symbolic(octal_str):
    """Convert octal permissions (e.g., 755) to symbolic (e.g., rwxr-xr-x)."""
    try:
        # Handle both 3-digit and 4-digit octal notation
        octal_str = octal_str.lstrip("0")
        if len(octal_str) > 4:
            raise ValueError("Invalid octal permission format")

        # If 4 digits, extract special bits and regular permissions
        if len(octal_str) == 4:
            special = int(octal_str[0])
            perms = octal_str[1:]
        else:
            special = 0
            perms = octal_str.zfill(3)

        # Ensure we have exactly 3 digits for user, group, other
        if len(perms) != 3:
            raise ValueError("Invalid octal permission format")

        owner = int(perms[0])
        group = int(perms[1])
        other = int(perms[2])

        # Validate digits are in range 0-7
        if not all(0 <= d <= 7 for d in [owner, group, other]):
            raise ValueError("Octal digits must be between 0 and 7")

        def digit_to_rwx(digit, position):
            """Convert a single octal digit to rwx format."""
            r = "r" if digit & 4 else "-"
            w = "w" if digit & 2 else "-"

            # Handle execute bit with special permissions
            if position == 0:  # owner
                if special & 4:  # setuid
                    x = "s" if digit & 1 else "S"
                else:
                    x = "x" if digit & 1 else "-"
            elif position == 1:  # group
                if special & 2:  # setgid
                    x = "s" if digit & 1 else "S"
                else:
                    x = "x" if digit & 1 else "-"
            else:  # other
                if special & 1:  # sticky
                    x = "t" if digit & 1 else "T"
                else:
                    x = "x" if digit & 1 else "-"

            return r + w + x

        result = (
            digit_to_rwx(owner, 0) + digit_to_rwx(group, 1) + digit_to_rwx(other, 2)
        )

        return result

    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid octal permission: {e}")


def symbolic_to_octal(symbolic):
    """Convert symbolic permissions (e.g., rwxr-xr-x) to octal (e.g., 755)."""
    if len(symbolic) != 9:
        raise ValueError("Symbolic permission must be exactly 9 characters")

    special = 0

    def rwx_to_digit(rwx, position):
        """Convert rwx string to octal digit."""
        nonlocal special
        digit = 0

        # Read permission
        if rwx[0] == "r":
            digit += 4
        elif rwx[0] != "-":
            raise ValueError(f"Invalid read permission: {rwx[0]}")

        # Write permission
        if rwx[1] == "w":
            digit += 2
        elif rwx[1] != "-":
            raise ValueError(f"Invalid write permission: {rwx[1]}")

        # Execute permission (can be x, s, S, t, T, or -)
        exec_char = rwx[2]
        if exec_char in ("x", "s", "t"):
            digit += 1

        # Special permissions
        if position == 0 and exec_char in ("s", "S"):  # setuid
            special += 4
        elif position == 1 and exec_char in ("s", "S"):  # setgid
            special += 2
        elif position == 2 and exec_char in ("t", "T"):  # sticky
            special += 1
        elif exec_char not in ("x", "-", "s", "S", "t", "T"):
            raise ValueError(f"Invalid execute permission: {exec_char}")

        return digit

    owner = rwx_to_digit(symbolic[0:3], 0)
    group = rwx_to_digit(symbolic[3:6], 1)
    other = rwx_to_digit(symbolic[6:9], 2)

    # Return with special bits if present
    if special > 0:
        return f"{special}{owner}{group}{other}"
    return f"{owner}{group}{other}"


def octal_to_binary(octal_str):
    """Convert octal permissions to binary representation."""
    try:
        octal_str = octal_str.lstrip("0") or "0"

        # Handle 4-digit octal
        if len(octal_str) == 4:
            special = int(octal_str[0])
            perms = octal_str[1:]
        else:
            special = 0
            perms = octal_str.zfill(3)

        result = []
        if special > 0:
            result.append(f"Special: {special:03b}")

        for i, digit in enumerate(perms):
            d = int(digit)
            label = ["Owner", "Group", "Other"][i]
            result.append(f"{label}: {d:03b}")

        return "\n".join(result)

    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid octal permission: {e}")


def explain_permissions(octal_str):
    """Explain what the permissions mean."""
    try:
        symbolic = octal_to_symbolic(octal_str)

        # Parse the permissions
        owner_perms = symbolic[0:3]
        group_perms = symbolic[3:6]
        other_perms = symbolic[6:9]

        def explain_rwx(rwx):
            perms = []
            if "r" in rwx:
                perms.append("read")
            if "w" in rwx:
                perms.append("write")
            if "x" in rwx or "s" in rwx or "t" in rwx:
                perms.append("execute")
            if "s" in rwx.lower():
                perms.append("setuid/setgid")
            if "t" in rwx.lower():
                perms.append("sticky")
            return ", ".join(perms) if perms else "none"

        lines = []
        lines.append(f"Octal: {octal_str}")
        lines.append(f"Symbolic: {symbolic}")
        lines.append(f"Owner (u): {owner_perms} ({explain_rwx(owner_perms)})")
        lines.append(f"Group (g): {group_perms} ({explain_rwx(group_perms)})")
        lines.append(f"Other (o): {other_perms} ({explain_rwx(other_perms)})")

        # Add chmod command
        lines.append(f"\nchmod command: chmod {octal_str} <file>")

        return "\n".join(lines)

    except Exception as e:
        raise ValueError(f"Error explaining permissions: {e}")


def calculate_permission(operation, perm1, perm2=None):
    """Calculate permission based on operation."""
    try:
        # Convert to integers
        perm1_int = int(perm1, 8) if isinstance(perm1, str) else perm1

        if operation == "add":
            if perm2 is None:
                raise ValueError("Add operation requires two permissions")
            perm2_int = int(perm2, 8) if isinstance(perm2, str) else perm2
            result = perm1_int | perm2_int
        elif operation == "remove":
            if perm2 is None:
                raise ValueError("Remove operation requires two permissions")
            perm2_int = int(perm2, 8) if isinstance(perm2, str) else perm2
            result = perm1_int & ~perm2_int
        elif operation == "mask":
            if perm2 is None:
                raise ValueError("Mask operation requires two permissions")
            perm2_int = int(perm2, 8) if isinstance(perm2, str) else perm2
            result = perm1_int & perm2_int
        else:
            raise ValueError(f"Unknown operation: {operation}")

        # Convert back to octal string (preserve leading zeros)
        return oct(result)[2:].zfill(3)

    except ValueError as e:
        raise ValueError(f"Invalid permission calculation: {e}")


def common_permissions():
    """List common permission patterns."""
    patterns = [
        ("644", "rw-r--r--", "Files: Owner read/write, others read only"),
        ("664", "rw-rw-r--", "Files: Owner and group read/write, others read only"),
        ("600", "rw-------", "Files: Owner read/write only (private)"),
        ("755", "rwxr-xr-x", "Executables/Dirs: Owner full, others read/execute"),
        (
            "775",
            "rwxrwxr-x",
            "Executables/Dirs: Owner and group full, others read/execute",
        ),
        ("700", "rwx------", "Executables/Dirs: Owner full only (private)"),
        ("777", "rwxrwxrwx", "Full access for everyone (dangerous!)"),
        ("000", "---------", "No access for anyone"),
    ]

    lines = []
    lines.append("Common Permission Patterns:")
    lines.append("")
    for octal, symbolic, description in patterns:
        lines.append(f"{octal} ({symbolic})  {description}")

    return "\n".join(lines)


def detect_format(value):
    """Detect if input is octal or symbolic."""
    # If it's 9 characters and contains rwx- characters, it's symbolic
    if len(value) == 9 and all(c in "rwxstST-" for c in value):
        return "symbolic"
    # Otherwise assume it's octal (3 or 4 digits)
    return "octal"


def handle_convert_command(args):
    """Handle permission conversion."""
    try:
        value = args.value
        target = args.to if hasattr(args, "to") and args.to else None

        # Auto-detect input format if target not specified
        if target is None:
            input_format = detect_format(value)
            if input_format == "octal":
                target = "symbolic"  # Convert octal to symbolic by default
            else:
                target = "octal"  # Convert symbolic to octal by default

        if target == "symbolic":
            result = octal_to_symbolic(value)
        elif target == "octal":
            result = symbolic_to_octal(value)
        elif target == "binary":
            # Binary needs octal input
            if detect_format(value) == "symbolic":
                value = symbolic_to_octal(value)
            result = octal_to_binary(value)
        else:
            print(f"Error: Unknown conversion target '{target}'", file=sys.stderr)
            sys.exit(1)

        print(result)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_explain_command(args):
    """Handle permission explanation."""
    try:
        result = explain_permissions(args.permission)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_calc_command(args):
    """Handle permission calculation."""
    try:
        result = calculate_permission(args.operation, args.perm1, args.perm2)
        symbolic = octal_to_symbolic(result)
        print(f"{result} ({symbolic})")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_common_command(args):
    """Handle common permissions list."""
    print(common_permissions())


def setup_parser(subparsers):
    """Setup the perm parser."""
    perm_parser = subparsers.add_parser(
        "perm",
        help="File permission conversions and calculations",
        description="Convert and calculate Unix/Linux file permissions between different formats.",
    )

    perm_subparsers = perm_parser.add_subparsers(
        dest="perm_command", required=True, help="Permission operation"
    )

    # Convert subcommand
    convert_parser = perm_subparsers.add_parser(
        "convert",
        help="Convert between permission formats",
        description="Auto-detects input format and converts accordingly. Use --to to specify output format.",
    )
    convert_parser.add_argument(
        "value", help="Permission value to convert (e.g., 755 or rwxr-xr-x)"
    )
    convert_parser.add_argument(
        "--to",
        choices=["symbolic", "octal", "binary"],
        help="Target format (auto-detected if not specified)",
    )
    convert_parser.set_defaults(func=handle_convert_command)

    # Explain subcommand
    explain_parser = perm_subparsers.add_parser(
        "explain", help="Explain what permissions mean"
    )
    explain_parser.add_argument(
        "permission", help="Octal permission to explain (e.g., 755)"
    )
    explain_parser.set_defaults(func=handle_explain_command)

    # Calculate subcommand
    calc_parser = perm_subparsers.add_parser("calc", help="Calculate permissions")
    calc_parser.add_argument(
        "operation",
        choices=["add", "remove", "mask"],
        help="Operation to perform",
    )
    calc_parser.add_argument("perm1", help="First permission (octal)")
    calc_parser.add_argument("perm2", help="Second permission (octal)", nargs="?")
    calc_parser.set_defaults(func=handle_calc_command)

    # Common subcommand
    common_parser = perm_subparsers.add_parser(
        "common", help="List common permission patterns"
    )
    common_parser.set_defaults(func=handle_common_command)
