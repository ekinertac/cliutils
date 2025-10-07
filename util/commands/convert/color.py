import re
import sys


def parse_color_input(value):
    """Parse color input and detect format."""
    value = value.strip()

    # Hex with # prefix: #ff0000
    if value.startswith("#"):
        hex_val = value[1:]
        if len(hex_val) == 6:
            return "hex", hex_val
        elif len(hex_val) == 3:
            # Short hex: expand #f00 to #ff0000
            return "hex", "".join([c * 2 for c in hex_val])

    # Hex with 0x prefix: 0xFF0000
    if value.lower().startswith("0x"):
        hex_val = value[2:]
        if len(hex_val) <= 6:
            return "hex", hex_val.zfill(6)

    # Plain hex: ff0000
    if re.match(r"^[0-9a-fA-F]{6}$", value):
        return "hex", value

    # RGB: rgb(255, 0, 0) or rgba(255, 0, 0, 1.0)
    rgb_match = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*[\d.]+)?\)", value)
    if rgb_match:
        r, g, b = map(int, rgb_match.groups())
        return "rgb", (r, g, b)

    # HSL: hsl(0, 100%, 50%) or hsla(0, 100%, 50%, 1.0)
    hsl_match = re.match(r"hsla?\((\d+),\s*(\d+)%,\s*(\d+)%(?:,\s*[\d.]+)?\)", value)
    if hsl_match:
        h, s, l = map(int, hsl_match.groups())
        return "hsl", (h, s, l)

    # Integer format: 16711680
    if re.match(r"^\d+$", value):
        num = int(value)
        if 0 <= num <= 16777215:  # Max RGB value (0xFFFFFF)
            return "int", num

    return None, None


def hex_to_rgb(hex_val):
    """Convert hex to RGB tuple."""
    hex_val = hex_val.lower()
    r = int(hex_val[0:2], 16)
    g = int(hex_val[2:4], 16)
    b = int(hex_val[4:6], 16)
    return r, g, b


def rgb_to_hex(r, g, b):
    """Convert RGB to hex string."""
    return f"{r:02x}{g:02x}{b:02x}"


def rgb_to_hsl(r, g, b):
    """Convert RGB to HSL."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    l = (max_c + min_c) / 2.0

    if max_c == min_c:
        h = s = 0.0
    else:
        d = max_c - min_c
        s = d / (2.0 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)

        if max_c == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_c == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6

    return int(h * 360), int(s * 100), int(l * 100)


def hsl_to_rgb(h, s, l):
    """Convert HSL to RGB."""
    h, s, l = h / 360.0, s / 100.0, l / 100.0

    if s == 0:
        r = g = b = l
    else:

        def hue_to_rgb(p, q, t):
            if t < 0:
                t += 1
            if t > 1:
                t -= 1
            if t < 1 / 6:
                return p + (q - p) * 6 * t
            if t < 1 / 2:
                return q
            if t < 2 / 3:
                return p + (q - p) * (2 / 3 - t) * 6
            return p

        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1 / 3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1 / 3)

    return int(r * 255), int(g * 255), int(b * 255)


def convert(value, target):
    """Convert color to target format."""
    fmt, data = parse_color_input(value)

    if fmt is None:
        print(f"Error: Unable to parse color value '{value}'", file=sys.stderr)
        sys.exit(1)

    # Convert to RGB as intermediate format
    if fmt == "hex":
        r, g, b = hex_to_rgb(data)
    elif fmt == "rgb":
        r, g, b = data
    elif fmt == "hsl":
        h, s, l = data
        r, g, b = hsl_to_rgb(h, s, l)
    elif fmt == "int":
        r = (data >> 16) & 0xFF
        g = (data >> 8) & 0xFF
        b = data & 0xFF

    # Convert from RGB to target format
    target = target.lower()
    if target in ["hex", "#"]:
        return f"#{rgb_to_hex(r, g, b)}"
    elif target in ["0x", "0xhex"]:
        return f"0x{rgb_to_hex(r, g, b).upper()}"
    elif target == "rgb":
        return f"rgb({r}, {g}, {b})"
    elif target == "hsl":
        h, s, l = rgb_to_hsl(r, g, b)
        return f"hsl({h}, {s}%, {l}%)"
    elif target in ["int", "integer", "decimal"]:
        return str((r << 16) | (g << 8) | b)
    else:
        print(f"Error: Unsupported target format '{target}'", file=sys.stderr)
        sys.exit(1)


def handle_command(args):
    """Handle color conversion command."""
    result = convert(args.value, args.target)
    print(result)


def setup_parser(subparsers):
    """Setup color conversion subparser."""
    color_parser = subparsers.add_parser(
        "color",
        help="Convert color formats",
        description="Convert between hex, RGB, HSL, and integer color formats.",
    )
    color_parser.add_argument(
        "value", type=str, help="Color value to convert (auto-detects format)"
    )
    color_parser.add_argument(
        "target",
        type=str,
        help="Target format: hex, 0x, rgb, hsl, int",
    )
    color_parser.set_defaults(func=handle_command)
