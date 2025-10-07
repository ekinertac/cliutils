import os
import platform
import subprocess
import sys


def get_pandoc_install_instructions():
    """Get OS-specific Pandoc installation instructions."""
    system = platform.system()

    if system == "Darwin":  # macOS
        return "brew install pandoc"
    elif system == "Linux":
        # Try to detect the distro
        try:
            with open("/etc/os-release") as f:
                os_info = f.read().lower()
                if "ubuntu" in os_info or "debian" in os_info:
                    return "sudo apt install pandoc"
                elif "fedora" in os_info or "rhel" in os_info or "centos" in os_info:
                    return "sudo dnf install pandoc"
                elif "arch" in os_info:
                    return "sudo pacman -S pandoc"
        except FileNotFoundError:
            pass
        return "sudo apt install pandoc  # or dnf/yum/pacman depending on your distro"
    elif system == "Windows":
        return "choco install pandoc  # or download from pandoc.org"
    else:
        return "Visit: https://pandoc.org/installing.html"


def check_pandoc_installed():
    """Check if Pandoc is installed."""
    try:
        subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def detect_format(filename):
    """Detect document format from file extension."""
    ext = os.path.splitext(filename)[1].lower()

    # Map extensions to Pandoc format names
    format_map = {
        ".md": "markdown",
        ".markdown": "markdown",
        ".html": "html",
        ".htm": "html",
        ".pdf": "pdf",
        ".docx": "docx",
        ".doc": "doc",
        ".odt": "odt",
        ".rtf": "rtf",
        ".txt": "plain",
        ".rst": "rst",
        ".tex": "latex",
        ".adoc": "asciidoc",
        ".org": "org",
        ".epub": "epub",
        ".ipynb": "ipynb",
    }

    return format_map.get(ext)


def convert_document(input_file, output_file, from_format=None, to_format=None):
    """Convert document using Pandoc."""
    # Build Pandoc command
    cmd = ["pandoc", input_file, "-o", output_file]

    # Add format specifications if provided
    if from_format:
        cmd.extend(["-f", from_format])
    if to_format:
        cmd.extend(["-t", to_format])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print("Error: Pandoc conversion failed", file=sys.stderr)
            if result.stderr:
                print(result.stderr, file=sys.stderr)
            return False

        return True
    except Exception as e:
        print(f"Error converting document: {e}", file=sys.stderr)
        return False


def handle_command(args):
    """Handle document conversion command."""
    input_file = args.input_file
    output_file = args.output_file

    # Check if Pandoc is installed
    if not check_pandoc_installed():
        print(
            "Error: Pandoc not installed. Install Pandoc to convert documents.",
            file=sys.stderr,
        )
        install_cmd = get_pandoc_install_instructions()
        print(f"Install with: {install_cmd}", file=sys.stderr)
        sys.exit(1)

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found", file=sys.stderr)
        sys.exit(1)

    # Detect formats
    input_format = detect_format(input_file)
    output_format = detect_format(output_file)

    # Use command-line format overrides if provided
    if args.from_format:
        input_format = args.from_format
    if args.to_format:
        output_format = args.to_format

    # Perform conversion
    success = convert_document(input_file, output_file, input_format, output_format)

    if success:
        print(f"Successfully converted '{input_file}' to '{output_file}'")
    else:
        sys.exit(1)


def setup_parser(subparsers):
    """Setup document conversion subparser."""
    doc_parser = subparsers.add_parser(
        "document",
        aliases=["doc"],
        help="Convert document formats",
        description="Convert between document formats using Pandoc (Markdown, HTML, PDF, DOCX, etc.).",
    )
    doc_parser.add_argument("input_file", type=str, help="Input document file")
    doc_parser.add_argument(
        "output_file", type=str, help="Output document file with desired format"
    )
    doc_parser.add_argument(
        "--from-format",
        "-f",
        type=str,
        help="Source format (auto-detected if not specified)",
    )
    doc_parser.add_argument(
        "--to-format",
        "-t",
        type=str,
        help="Target format (auto-detected if not specified)",
    )
    doc_parser.set_defaults(func=handle_command)
