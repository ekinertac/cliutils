import os
import platform
import subprocess
import sys


def convert_image(input_file, output_file):
    """Convert image using Pillow."""
    try:
        from PIL import Image
    except ImportError:
        print(
            "Error: Pillow library not installed. Install with: pip install Pillow",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        with Image.open(input_file) as img:
            # Convert RGBA to RGB if saving to formats that don't support alpha
            if output_file.lower().endswith((".jpg", ".jpeg")):
                if img.mode in ("RGBA", "LA", "P"):
                    # Create white background
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode == "P":
                        img = img.convert("RGBA")
                    background.paste(
                        img, mask=img.split()[-1] if img.mode == "RGBA" else None
                    )
                    img = background
                else:
                    img = img.convert("RGB")

            img.save(output_file)
        return True
    except Exception as e:
        print(f"Error converting image: {e}", file=sys.stderr)
        return False


def get_ffmpeg_install_instructions():
    """Get OS-specific FFmpeg installation instructions."""
    system = platform.system()

    if system == "Darwin":  # macOS
        return "brew install ffmpeg"
    elif system == "Linux":
        # Try to detect the distro
        try:
            with open("/etc/os-release") as f:
                os_info = f.read().lower()
                if "ubuntu" in os_info or "debian" in os_info:
                    return "sudo apt install ffmpeg"
                elif "fedora" in os_info or "rhel" in os_info or "centos" in os_info:
                    return "sudo dnf install ffmpeg"
                elif "arch" in os_info:
                    return "sudo pacman -S ffmpeg"
        except FileNotFoundError:
            pass
        return "sudo apt install ffmpeg  # or dnf/yum/pacman depending on your distro"
    elif system == "Windows":
        return "choco install ffmpeg  # or download from ffmpeg.org"
    else:
        return "Visit: https://ffmpeg.org/download.html"


def convert_video_audio(input_file, output_file):
    """Convert video/audio using FFmpeg."""
    # Check if ffmpeg is installed
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(
            "Error: FFmpeg not installed. Install FFmpeg to convert video/audio files.",
            file=sys.stderr,
        )
        install_cmd = get_ffmpeg_install_instructions()
        print(f"Install with: {install_cmd}", file=sys.stderr)
        sys.exit(1)

    try:
        # Run ffmpeg conversion
        cmd = [
            "ffmpeg",
            "-i",
            input_file,
            "-y",  # Overwrite output file
            output_file,
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print("Error: FFmpeg conversion failed", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            return False

        return True
    except Exception as e:
        print(f"Error converting file: {e}", file=sys.stderr)
        return False


def detect_file_type(filename):
    """Detect file type based on extension."""
    ext = os.path.splitext(filename)[1].lower()

    image_formats = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".ico"]
    video_formats = [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm", ".m4v"]
    audio_formats = [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"]

    if ext in image_formats:
        return "image"
    elif ext in video_formats:
        return "video"
    elif ext in audio_formats:
        return "audio"
    else:
        return "unknown"


def handle_command(args):
    """Handle file conversion command."""
    input_file = args.input_file
    output_file = args.output_file

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found", file=sys.stderr)
        sys.exit(1)

    # Detect file types
    input_type = detect_file_type(input_file)
    output_type = detect_file_type(output_file)

    if input_type == "unknown":
        print("Error: Unsupported input file format", file=sys.stderr)
        sys.exit(1)

    if output_type == "unknown":
        print("Error: Unsupported output file format", file=sys.stderr)
        sys.exit(1)

    # Perform conversion based on type
    success = False
    if input_type == "image" and output_type == "image":
        success = convert_image(input_file, output_file)
    elif input_type in ["video", "audio"] or output_type in ["video", "audio"]:
        success = convert_video_audio(input_file, output_file)
    else:
        print(
            f"Error: Cannot convert from {input_type} to {output_type}",
            file=sys.stderr,
        )
        sys.exit(1)

    if success:
        print(f"Successfully converted '{input_file}' to '{output_file}'")
    else:
        sys.exit(1)


def setup_parser(subparsers):
    """Setup file conversion subparser."""
    file_parser = subparsers.add_parser(
        "file",
        help="Convert file formats",
        description="Convert between image, video, and audio file formats.",
    )
    file_parser.add_argument("input_file", type=str, help="Input file path")
    file_parser.add_argument(
        "output_file", type=str, help="Output file path with desired format"
    )
    file_parser.set_defaults(func=handle_command)
