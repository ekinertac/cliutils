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


def is_pandoc_installed():
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


# Skip all tests if Pandoc is not installed
import pytest

pandoc_installed = is_pandoc_installed()
skip_if_no_pandoc = pytest.mark.skipif(
    not pandoc_installed, reason="Pandoc not installed"
)


# ============================================================================
# MARKDOWN CONVERSION TESTS
# ============================================================================


@skip_if_no_pandoc
def test_convert_document_md_to_html():
    """Test converting Markdown to HTML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.md")
        output_file = os.path.join(tmpdir, "test.html")

        # Create test Markdown
        with open(input_file, "w") as f:
            f.write("# Hello\n\nThis is **bold** text.")

        # Convert
        result = run_util_command(["convert", "document", input_file, output_file])
        assert result.returncode == 0
        assert "Successfully converted" in result.stdout
        assert os.path.exists(output_file)

        # Check output
        with open(output_file) as f:
            content = f.read()
            assert "<h1" in content
            assert "<strong>bold</strong>" in content


@skip_if_no_pandoc
def test_convert_document_md_to_html_alias():
    """Test using doc alias."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.md")
        output_file = os.path.join(tmpdir, "test.html")

        with open(input_file, "w") as f:
            f.write("# Test")

        # Use 'doc' alias instead of 'document'
        result = run_util_command(["convert", "doc", input_file, output_file])
        assert result.returncode == 0
        assert os.path.exists(output_file)


@skip_if_no_pandoc
def test_convert_document_html_to_md():
    """Test converting HTML to Markdown."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.html")
        output_file = os.path.join(tmpdir, "test.md")

        # Create test HTML
        with open(input_file, "w") as f:
            f.write("<h1>Hello</h1><p>This is <strong>bold</strong> text.</p>")

        # Convert
        result = run_util_command(["convert", "document", input_file, output_file])
        assert result.returncode == 0
        assert os.path.exists(output_file)

        # Check output
        with open(output_file) as f:
            content = f.read()
            assert "Hello" in content
            assert "**bold**" in content or "bold" in content


@skip_if_no_pandoc
def test_convert_document_md_with_lists():
    """Test converting Markdown with lists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.md")
        output_file = os.path.join(tmpdir, "test.html")

        # Create Markdown with lists
        with open(input_file, "w") as f:
            f.write("# Items\n\n- Item 1\n- Item 2\n- Item 3")

        # Convert
        result = run_util_command(["convert", "document", input_file, output_file])
        assert result.returncode == 0

        # Check output
        with open(output_file) as f:
            content = f.read()
            assert "<ul>" in content or "<li>" in content


@skip_if_no_pandoc
def test_convert_document_md_with_code():
    """Test converting Markdown with code blocks."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.md")
        output_file = os.path.join(tmpdir, "test.html")

        # Create Markdown with code
        with open(input_file, "w") as f:
            f.write("# Code\n\n```python\nprint('hello')\n```")

        # Convert
        result = run_util_command(["convert", "document", input_file, output_file])
        assert result.returncode == 0

        # Check output
        with open(output_file) as f:
            content = f.read()
            assert "hello" in content


@skip_if_no_pandoc
def test_convert_document_md_with_links():
    """Test converting Markdown with links."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.md")
        output_file = os.path.join(tmpdir, "test.html")

        # Create Markdown with links
        with open(input_file, "w") as f:
            f.write("[Google](https://google.com)")

        # Convert
        result = run_util_command(["convert", "document", input_file, output_file])
        assert result.returncode == 0

        # Check output
        with open(output_file) as f:
            content = f.read()
            assert "<a" in content
            assert "google.com" in content


# ============================================================================
# FORMAT SPECIFICATION TESTS
# ============================================================================


@skip_if_no_pandoc
def test_convert_document_explicit_formats():
    """Test with explicit format specifications."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.md")
        output_file = os.path.join(tmpdir, "test.html")

        with open(input_file, "w") as f:
            f.write("# Test")

        # Use explicit format flags
        result = run_util_command(
            [
                "convert",
                "document",
                input_file,
                output_file,
                "-f",
                "markdown",
                "-t",
                "html",
            ]
        )
        assert result.returncode == 0
        assert os.path.exists(output_file)


@skip_if_no_pandoc
def test_convert_document_long_format_flags():
    """Test with long format flag names."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.md")
        output_file = os.path.join(tmpdir, "test.html")

        with open(input_file, "w") as f:
            f.write("# Test")

        # Use long format flags
        result = run_util_command(
            [
                "convert",
                "document",
                input_file,
                output_file,
                "--from-format",
                "markdown",
                "--to-format",
                "html",
            ]
        )
        assert result.returncode == 0
        assert os.path.exists(output_file)


# ============================================================================
# ROUNDTRIP TESTS
# ============================================================================


@skip_if_no_pandoc
def test_convert_document_roundtrip_md_html_md():
    """Test roundtrip conversion: Markdown → HTML → Markdown."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_file = os.path.join(tmpdir, "original.md")
        html_file = os.path.join(tmpdir, "intermediate.html")
        final_file = os.path.join(tmpdir, "final.md")

        # Create original Markdown
        original_content = "# Hello\n\nThis is **bold** text."
        with open(original_file, "w") as f:
            f.write(original_content)

        # Convert to HTML
        result1 = run_util_command(["convert", "document", original_file, html_file])
        assert result1.returncode == 0

        # Convert back to Markdown
        result2 = run_util_command(["convert", "document", html_file, final_file])
        assert result2.returncode == 0

        # Check that content is preserved (format may vary)
        with open(final_file) as f:
            content = f.read()
            assert "Hello" in content
            assert "bold" in content


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================


@skip_if_no_pandoc
def test_convert_document_input_not_found():
    """Test error when input file doesn't exist."""
    result = run_util_command(
        ["convert", "document", "/tmp/nonexistent.md", "/tmp/output.html"]
    )
    assert result.returncode != 0
    assert "not found" in result.stderr.lower()


@skip_if_no_pandoc
def test_convert_document_invalid_markdown():
    """Test with malformed input (should still work or fail gracefully)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.md")
        output_file = os.path.join(tmpdir, "test.html")

        # Create somewhat malformed Markdown (Pandoc is usually forgiving)
        with open(input_file, "w") as f:
            f.write("# Unclosed **bold")

        # Convert - should still work or fail gracefully
        result = run_util_command(["convert", "document", input_file, output_file])
        # Pandoc usually handles this, so we just check it doesn't crash
        assert result.returncode in [0, 1]


# ============================================================================
# HELP TESTS
# ============================================================================


def test_convert_document_help():
    """Test document conversion help (doesn't require Pandoc)."""
    result = run_util_command(["convert", "document", "--help"])
    assert result.returncode == 0
    assert "document" in result.stdout.lower()
    assert "pandoc" in result.stdout.lower()


def test_convert_document_no_arguments():
    """Test error when no arguments provided."""
    result = run_util_command(["convert", "document"])
    assert result.returncode != 0
    assert "required" in result.stderr.lower() or "error" in result.stderr.lower()


@skip_if_no_pandoc
def test_convert_document_missing_output():
    """Test error when output file argument is missing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.md")
        with open(input_file, "w") as f:
            f.write("# Test")

        result = run_util_command(["convert", "document", input_file])
        assert result.returncode != 0
        assert "required" in result.stderr.lower() or "error" in result.stderr.lower()


# ============================================================================
# INSTALLATION CHECK TEST
# ============================================================================


def test_convert_document_pandoc_not_installed():
    """Test error message when Pandoc is not installed."""
    if pandoc_installed:
        pytest.skip("Pandoc is installed, cannot test error message")

    result = run_util_command(["convert", "document", "/tmp/test.md", "/tmp/test.html"])
    assert result.returncode != 0
    assert "pandoc" in result.stderr.lower()
    assert "install" in result.stderr.lower()
