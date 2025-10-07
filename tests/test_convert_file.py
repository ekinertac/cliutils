import os
import subprocess
import tempfile


def run_util_command(args):
    """Helper function to run util command as a subprocess."""
    result = subprocess.run(
        ["python", "-m", "util.main"] + args,
        capture_output=True,
        text=True,
    )
    return result


def create_test_image(filepath, format="PNG", size=(100, 100), color="red"):
    """Create a test image using Pillow."""
    try:
        from PIL import Image

        img = Image.new("RGB", size, color=color)
        img.save(filepath, format=format)
        return True
    except Exception:
        return False


# ============================================================================
# IMAGE CONVERSION TESTS
# ============================================================================


def test_convert_file_png_to_jpg():
    """Test converting PNG to JPG."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.png")
        output_file = os.path.join(tmpdir, "test.jpg")

        # Create test PNG
        assert create_test_image(input_file, "PNG")

        # Convert
        result = run_util_command(["convert", "file", input_file, output_file])
        assert result.returncode == 0
        assert "Successfully converted" in result.stdout
        assert os.path.exists(output_file)


def test_convert_file_jpg_to_png():
    """Test converting JPG to PNG."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.jpg")
        output_file = os.path.join(tmpdir, "test.png")

        # Create test JPG
        assert create_test_image(input_file, "JPEG")

        # Convert
        result = run_util_command(["convert", "file", input_file, output_file])
        assert result.returncode == 0
        assert "Successfully converted" in result.stdout
        assert os.path.exists(output_file)


def test_convert_file_png_to_webp():
    """Test converting PNG to WEBP."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.png")
        output_file = os.path.join(tmpdir, "test.webp")

        # Create test PNG
        assert create_test_image(input_file, "PNG")

        # Convert
        result = run_util_command(["convert", "file", input_file, output_file])
        assert result.returncode == 0
        assert "Successfully converted" in result.stdout
        assert os.path.exists(output_file)


def test_convert_file_jpg_to_bmp():
    """Test converting JPG to BMP."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.jpg")
        output_file = os.path.join(tmpdir, "test.bmp")

        # Create test JPG
        assert create_test_image(input_file, "JPEG")

        # Convert
        result = run_util_command(["convert", "file", input_file, output_file])
        assert result.returncode == 0
        assert "Successfully converted" in result.stdout
        assert os.path.exists(output_file)


def test_convert_file_png_to_gif():
    """Test converting PNG to GIF."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.png")
        output_file = os.path.join(tmpdir, "test.gif")

        # Create test PNG
        assert create_test_image(input_file, "PNG")

        # Convert
        result = run_util_command(["convert", "file", input_file, output_file])
        assert result.returncode == 0
        assert "Successfully converted" in result.stdout
        assert os.path.exists(output_file)


def test_convert_file_different_colors():
    """Test converting images with different colors."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "blue.png")
        output_file = os.path.join(tmpdir, "blue.jpg")

        # Create blue test image
        assert create_test_image(input_file, "PNG", color="blue")

        # Convert
        result = run_util_command(["convert", "file", input_file, output_file])
        assert result.returncode == 0
        assert os.path.exists(output_file)


def test_convert_file_different_sizes():
    """Test converting images with different sizes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "large.png")
        output_file = os.path.join(tmpdir, "large.jpg")

        # Create larger test image
        assert create_test_image(input_file, "PNG", size=(500, 300))

        # Convert
        result = run_util_command(["convert", "file", input_file, output_file])
        assert result.returncode == 0
        assert os.path.exists(output_file)


def test_convert_file_rgba_to_jpg():
    """Test converting RGBA PNG to JPG (should handle transparency)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "rgba.png")
        output_file = os.path.join(tmpdir, "rgba.jpg")

        # Create RGBA test image
        try:
            from PIL import Image

            img = Image.new("RGBA", (100, 100), color=(255, 0, 0, 128))
            img.save(input_file, "PNG")
        except Exception:
            return  # Skip if can't create RGBA

        # Convert
        result = run_util_command(["convert", "file", input_file, output_file])
        assert result.returncode == 0
        assert os.path.exists(output_file)


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================


def test_convert_file_input_not_found():
    """Test error when input file doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "nonexistent.png")
        output_file = os.path.join(tmpdir, "output.jpg")

        result = run_util_command(["convert", "file", input_file, output_file])
        assert result.returncode != 0
        assert "not found" in result.stderr.lower() or "error" in result.stderr.lower()


def test_convert_file_unsupported_input_format():
    """Test error with unsupported input format."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.xyz")
        output_file = os.path.join(tmpdir, "test.jpg")

        # Create a dummy file with unsupported extension
        with open(input_file, "w") as f:
            f.write("dummy")

        result = run_util_command(["convert", "file", input_file, output_file])
        assert result.returncode != 0
        assert (
            "unsupported" in result.stderr.lower() or "error" in result.stderr.lower()
        )


def test_convert_file_unsupported_output_format():
    """Test error with unsupported output format."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.png")
        output_file = os.path.join(tmpdir, "test.xyz")

        # Create test PNG
        assert create_test_image(input_file, "PNG")

        result = run_util_command(["convert", "file", input_file, output_file])
        assert result.returncode != 0
        assert (
            "unsupported" in result.stderr.lower() or "error" in result.stderr.lower()
        )


def test_convert_file_corrupted_image():
    """Test error with corrupted image file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "corrupted.png")
        output_file = os.path.join(tmpdir, "output.jpg")

        # Create a corrupted file
        with open(input_file, "w") as f:
            f.write("This is not a valid PNG file")

        result = run_util_command(["convert", "file", input_file, output_file])
        assert result.returncode != 0
        assert "error" in result.stderr.lower()


# ============================================================================
# HELP AND USAGE TESTS
# ============================================================================


def test_convert_file_help():
    """Test file conversion help."""
    result = run_util_command(["convert", "file", "--help"])
    assert result.returncode == 0
    assert "file" in result.stdout.lower()
    assert "input_file" in result.stdout.lower()
    assert "output_file" in result.stdout.lower()


def test_convert_file_no_arguments():
    """Test error when no arguments provided."""
    result = run_util_command(["convert", "file"])
    assert result.returncode != 0
    assert "required" in result.stderr.lower() or "error" in result.stderr.lower()


def test_convert_file_missing_output():
    """Test error when output file argument is missing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.png")
        assert create_test_image(input_file, "PNG")

        result = run_util_command(["convert", "file", input_file])
        assert result.returncode != 0
        assert "required" in result.stderr.lower() or "error" in result.stderr.lower()


# ============================================================================
# ROUNDTRIP TESTS
# ============================================================================


def test_convert_file_roundtrip_png_jpg_png():
    """Test converting PNG -> JPG -> PNG (lossy roundtrip)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original = os.path.join(tmpdir, "original.png")
        intermediate = os.path.join(tmpdir, "intermediate.jpg")
        final = os.path.join(tmpdir, "final.png")

        # Create original PNG
        assert create_test_image(original, "PNG")

        # Convert to JPG
        result1 = run_util_command(["convert", "file", original, intermediate])
        assert result1.returncode == 0
        assert os.path.exists(intermediate)

        # Convert back to PNG
        result2 = run_util_command(["convert", "file", intermediate, final])
        assert result2.returncode == 0
        assert os.path.exists(final)


def test_convert_file_same_format_png_to_png():
    """Test converting PNG to PNG (should work as a copy)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "input.png")
        output_file = os.path.join(tmpdir, "output.png")

        # Create test PNG
        assert create_test_image(input_file, "PNG")

        # Convert
        result = run_util_command(["convert", "file", input_file, output_file])
        assert result.returncode == 0
        assert os.path.exists(output_file)


# ============================================================================
# MULTIPLE FORMAT TESTS
# ============================================================================


def test_convert_file_multiple_formats_from_png():
    """Test converting one PNG to multiple formats."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "source.png")
        assert create_test_image(input_file, "PNG")

        formats = ["jpg", "bmp", "gif", "webp"]
        for fmt in formats:
            output_file = os.path.join(tmpdir, f"output.{fmt}")
            result = run_util_command(["convert", "file", input_file, output_file])
            assert result.returncode == 0, f"Failed to convert to {fmt}"
            assert os.path.exists(output_file), f"Output file {fmt} not created"


def test_convert_file_case_insensitive_extensions():
    """Test that file extensions are case-insensitive."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.PNG")
        output_file = os.path.join(tmpdir, "test.JPG")

        # Create test image with uppercase extension
        assert create_test_image(input_file, "PNG")

        # Convert
        result = run_util_command(["convert", "file", input_file, output_file])
        assert result.returncode == 0
        assert os.path.exists(output_file)
