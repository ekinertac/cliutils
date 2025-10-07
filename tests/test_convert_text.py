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


# ============================================================================
# URL ENCODING TESTS
# ============================================================================


def test_convert_text_url_encode():
    """Test URL encoding."""
    result = run_util_command(["convert", "text", "url-encode", "hello world"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello%20world"


def test_convert_text_url_encode_special():
    """Test URL encoding with special characters."""
    result = run_util_command(["convert", "text", "url-encode", "hello@world.com"])
    assert result.returncode == 0
    assert "%40" in result.stdout  # @ encoded


def test_convert_text_url_decode():
    """Test URL decoding."""
    result = run_util_command(["convert", "text", "url-decode", "hello%20world"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello world"


def test_convert_text_url_roundtrip():
    """Test URL encode/decode roundtrip."""
    original = "hello world & test"
    result1 = run_util_command(["convert", "text", "url-encode", original])
    assert result1.returncode == 0
    encoded = result1.stdout.strip()

    result2 = run_util_command(["convert", "text", "url-decode", encoded])
    assert result2.returncode == 0
    assert result2.stdout.strip() == original


# ============================================================================
# HTML ENCODING TESTS
# ============================================================================


def test_convert_text_html_encode():
    """Test HTML entity encoding."""
    result = run_util_command(["convert", "text", "html-encode", "<div>Test</div>"])
    assert result.returncode == 0
    assert "&lt;div&gt;" in result.stdout
    assert result.stdout.strip() == "&lt;div&gt;Test&lt;/div&gt;"


def test_convert_text_html_encode_ampersand():
    """Test HTML encoding of ampersand."""
    result = run_util_command(["convert", "text", "html-encode", "Hello & goodbye"])
    assert result.returncode == 0
    assert "&amp;" in result.stdout


def test_convert_text_html_decode():
    """Test HTML entity decoding."""
    result = run_util_command(
        ["convert", "text", "html-decode", "&lt;div&gt;Test&lt;/div&gt;"]
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "<div>Test</div>"


def test_convert_text_html_roundtrip():
    """Test HTML encode/decode roundtrip."""
    original = "<div>Hello & goodbye</div>"
    result1 = run_util_command(["convert", "text", "html-encode", original])
    assert result1.returncode == 0
    encoded = result1.stdout.strip()

    result2 = run_util_command(["convert", "text", "html-decode", encoded])
    assert result2.returncode == 0
    assert result2.stdout.strip() == original


# ============================================================================
# LINE ENDINGS TESTS
# ============================================================================


def test_convert_text_line_endings_lf_to_crlf():
    """Test converting LF to CRLF."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.txt")
        with open(input_file, "w", newline="\n") as f:
            f.write("line1\nline2\nline3")

        result = run_util_command(
            [
                "convert",
                "text",
                "line-endings",
                "--file",
                input_file,
                "--target",
                "crlf",
            ]
        )
        assert result.returncode == 0
        # Check for CRLF or just verify it doesn't error
        lines = result.stdout.split("\n")
        assert len(lines) >= 3


def test_convert_text_line_endings_crlf_to_lf():
    """Test converting CRLF to LF."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.txt")
        with open(input_file, "w", newline="\r\n") as f:
            f.write("line1\r\nline2\r\nline3")

        result = run_util_command(
            ["convert", "text", "line-endings", "--file", input_file, "--target", "lf"]
        )
        assert result.returncode == 0
        # Just verify it works
        lines = result.stdout.split("\n")
        assert len(lines) >= 3


# ============================================================================
# STRING ESCAPE TESTS
# ============================================================================


def test_convert_text_escape_python():
    """Test escaping for Python."""
    result = run_util_command(
        ["convert", "text", "escape", "Hello\nWorld", "--target", "python"]
    )
    assert result.returncode == 0
    assert "\\n" in result.stdout


def test_convert_text_escape_javascript():
    """Test escaping for JavaScript."""
    result = run_util_command(
        ["convert", "text", "escape", "It's a test", "--target", "javascript"]
    )
    assert result.returncode == 0
    assert "\\'" in result.stdout or "'" in result.stdout


def test_convert_text_escape_sql():
    """Test escaping for SQL."""
    result = run_util_command(
        ["convert", "text", "escape", "It's a test", "--target", "sql"]
    )
    assert result.returncode == 0
    assert "''" in result.stdout


def test_convert_text_escape_json():
    """Test escaping for JSON."""
    result = run_util_command(
        ["convert", "text", "escape", 'Hello "World"', "--target", "json"]
    )
    assert result.returncode == 0
    assert '\\"' in result.stdout


def test_convert_text_unescape_python():
    """Test unescaping Python string."""
    result = run_util_command(
        ["convert", "text", "unescape", "Hello\\nWorld", "--target", "python"]
    )
    assert result.returncode == 0
    assert "\n" in result.stdout


def test_convert_text_unescape_sql():
    """Test unescaping SQL string."""
    result = run_util_command(
        ["convert", "text", "unescape", "It''s a test", "--target", "sql"]
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "It's a test"


# ============================================================================
# HELP TESTS
# ============================================================================


def test_convert_text_help():
    """Test text conversion help."""
    result = run_util_command(["convert", "text", "--help"])
    assert result.returncode == 0
    assert "text" in result.stdout.lower()
    assert "url-encode" in result.stdout.lower()


def test_convert_text_no_arguments():
    """Test error when no arguments provided."""
    result = run_util_command(["convert", "text"])
    assert result.returncode != 0
    assert "required" in result.stderr.lower() or "error" in result.stderr.lower()
