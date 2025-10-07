import subprocess


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


def test_encode_url_encode():
    """Test URL encoding."""
    result = run_util_command(["encode", "url", "encode", "hello world"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello%20world"


def test_encode_url_decode():
    """Test URL decoding."""
    result = run_util_command(["encode", "url", "decode", "hello%20world"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello world"


def test_encode_url_roundtrip():
    """Test URL encode/decode roundtrip."""
    original = "hello world & test=123"
    result1 = run_util_command(["encode", "url", "encode", original])
    assert result1.returncode == 0
    encoded = result1.stdout.strip()

    result2 = run_util_command(["encode", "url", "decode", encoded])
    assert result2.returncode == 0
    assert result2.stdout.strip() == original


# ============================================================================
# HTML ENCODING TESTS
# ============================================================================


def test_encode_html_encode():
    """Test HTML entity encoding."""
    result = run_util_command(["encode", "html", "encode", "<div>Test</div>"])
    assert result.returncode == 0
    assert "&lt;div&gt;" in result.stdout
    assert result.stdout.strip() == "&lt;div&gt;Test&lt;/div&gt;"


def test_encode_html_decode():
    """Test HTML entity decoding."""
    result = run_util_command(
        ["encode", "html", "decode", "&lt;div&gt;Test&lt;/div&gt;"]
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "<div>Test</div>"


def test_encode_html_ampersand():
    """Test HTML encoding of ampersand."""
    result = run_util_command(["encode", "html", "encode", "Hello & goodbye"])
    assert result.returncode == 0
    assert "&amp;" in result.stdout


# ============================================================================
# UNICODE ESCAPE TESTS
# ============================================================================


def test_encode_unicode_encode():
    """Test Unicode escape encoding."""
    result = run_util_command(["encode", "unicode", "encode", "Hello"])
    assert result.returncode == 0
    assert "Hello" in result.stdout  # ASCII characters remain as-is


def test_encode_unicode_decode():
    """Test Unicode escape decoding."""
    result = run_util_command(["encode", "unicode", "decode", "Hello"])
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello"


def test_encode_unicode_alias():
    """Test using uni alias."""
    result = run_util_command(["encode", "uni", "encode", "test"])
    assert result.returncode == 0


# ============================================================================
# HEX ENCODING TESTS
# ============================================================================


def test_encode_hex_encode():
    """Test hex encoding."""
    result = run_util_command(["encode", "hex", "encode", "test"])
    assert result.returncode == 0
    assert result.stdout.strip() == "74657374"


def test_encode_hex_decode():
    """Test hex decoding."""
    result = run_util_command(["encode", "hex", "decode", "74657374"])
    assert result.returncode == 0
    assert result.stdout.strip() == "test"


def test_encode_hex_roundtrip():
    """Test hex encode/decode roundtrip."""
    original = "Hello World"
    result1 = run_util_command(["encode", "hex", "encode", original])
    assert result1.returncode == 0
    encoded = result1.stdout.strip()

    result2 = run_util_command(["encode", "hex", "decode", encoded])
    assert result2.returncode == 0
    assert result2.stdout.strip() == original


# ============================================================================
# HEXDUMP TESTS
# ============================================================================


def test_encode_hexdump_basic():
    """Test basic hex dump."""
    result = run_util_command(["encode", "hexdump", "Hello, World!"])
    assert result.returncode == 0
    assert "00000000" in result.stdout
    assert "48 65 6c 6c 6f" in result.stdout  # "Hello" in hex
    assert "|Hello, World!|" in result.stdout


def test_encode_hexdump_width():
    """Test hex dump with custom width."""
    result = run_util_command(["encode", "hexdump", "test", "--width", "8"])
    assert result.returncode == 0
    assert "00000000" in result.stdout


def test_encode_hexdump_alias():
    """Test using dump alias."""
    result = run_util_command(["encode", "dump", "test"])
    assert result.returncode == 0
    assert "00000000" in result.stdout


# ============================================================================
# BASE64 TESTS
# ============================================================================


def test_encode_base64_encode():
    """Test base64 encoding."""
    result = run_util_command(["encode", "base64", "encode", "Hello, World!"])
    assert result.returncode == 0
    assert result.stdout.strip() == "SGVsbG8sIFdvcmxkIQ=="


def test_encode_base64_decode():
    """Test base64 decoding."""
    result = run_util_command(["encode", "base64", "decode", "SGVsbG8sIFdvcmxkIQ=="])
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, World!"


def test_encode_base64_alias():
    """Test using b64 alias."""
    result = run_util_command(["encode", "b64", "encode", "test"])
    assert result.returncode == 0


def test_encode_base64_roundtrip():
    """Test base64 roundtrip."""
    original = "Test 123!"
    result1 = run_util_command(["encode", "base64", "encode", original])
    assert result1.returncode == 0
    encoded = result1.stdout.strip()

    result2 = run_util_command(["encode", "base64", "decode", encoded])
    assert result2.returncode == 0
    assert result2.stdout.strip() == original


# ============================================================================
# BASE32 TESTS
# ============================================================================


def test_encode_base32_encode():
    """Test base32 encoding."""
    result = run_util_command(["encode", "base32", "encode", "test"])
    assert result.returncode == 0
    assert "=" in result.stdout or len(result.stdout.strip()) > 0


def test_encode_base32_decode():
    """Test base32 decoding."""
    result1 = run_util_command(["encode", "base32", "encode", "test"])
    encoded = result1.stdout.strip()

    result2 = run_util_command(["encode", "base32", "decode", encoded])
    assert result2.returncode == 0
    assert result2.stdout.strip() == "test"


def test_encode_base32_alias():
    """Test using b32 alias."""
    result = run_util_command(["encode", "b32", "encode", "test"])
    assert result.returncode == 0


# ============================================================================
# BINARY TESTS
# ============================================================================


def test_encode_binary_encode():
    """Test binary encoding."""
    result = run_util_command(["encode", "binary", "encode", "Hi"])
    assert result.returncode == 0
    assert "01001000 01101001" in result.stdout


def test_encode_binary_decode():
    """Test binary decoding."""
    result = run_util_command(["encode", "binary", "decode", "01001000 01101001"])
    assert result.returncode == 0
    assert result.stdout.strip() == "Hi"


def test_encode_binary_alias():
    """Test using bin alias."""
    result = run_util_command(["encode", "bin", "encode", "A"])
    assert result.returncode == 0
    assert "01000001" in result.stdout


def test_encode_binary_roundtrip():
    """Test binary roundtrip."""
    original = "Test"
    result1 = run_util_command(["encode", "binary", "encode", original])
    assert result1.returncode == 0
    encoded = result1.stdout.strip()

    result2 = run_util_command(["encode", "binary", "decode", encoded])
    assert result2.returncode == 0
    assert result2.stdout.strip() == original


# ============================================================================
# ROT13 TESTS
# ============================================================================


def test_encode_rot13_encode():
    """Test ROT13 encoding."""
    result = run_util_command(["encode", "rot13", "Hello World"])
    assert result.returncode == 0
    assert result.stdout.strip() == "Uryyb Jbeyq"


def test_encode_rot13_roundtrip():
    """Test ROT13 double application (should give original)."""
    original = "Hello World"
    result1 = run_util_command(["encode", "rot13", original])
    assert result1.returncode == 0
    encoded = result1.stdout.strip()

    result2 = run_util_command(["encode", "rot13", encoded])
    assert result2.returncode == 0
    assert result2.stdout.strip() == original


def test_encode_rot13_numbers_unchanged():
    """Test ROT13 doesn't change numbers."""
    result = run_util_command(["encode", "rot13", "Test123"])
    assert result.returncode == 0
    assert "123" in result.stdout


# ============================================================================
# MORSE CODE TESTS
# ============================================================================


def test_encode_morse_encode():
    """Test Morse code encoding."""
    result = run_util_command(["encode", "morse", "encode", "SOS"])
    assert result.returncode == 0
    assert result.stdout.strip() == "... --- ..."


def test_encode_morse_decode():
    """Test Morse code decoding."""
    result = run_util_command(["encode", "morse", "decode", "... --- ..."])
    assert result.returncode == 0
    assert result.stdout.strip() == "SOS"


def test_encode_morse_roundtrip():
    """Test Morse code roundtrip."""
    original = "HELLO"
    result1 = run_util_command(["encode", "morse", "encode", original])
    assert result1.returncode == 0
    encoded = result1.stdout.strip()

    result2 = run_util_command(["encode", "morse", "decode", encoded])
    assert result2.returncode == 0
    assert result2.stdout.strip() == original


def test_encode_morse_with_spaces():
    """Test Morse code with word spaces."""
    result = run_util_command(["encode", "morse", "encode", "HI THERE"])
    assert result.returncode == 0
    assert "/" in result.stdout  # Word separator


# ============================================================================
# HELP TESTS
# ============================================================================


def test_encode_help():
    """Test encode command help."""
    result = run_util_command(["encode", "--help"])
    assert result.returncode == 0
    assert "encode" in result.stdout.lower()


def test_encode_url_help():
    """Test URL encoding help."""
    result = run_util_command(["encode", "url", "--help"])
    assert result.returncode == 0
    assert "url" in result.stdout.lower()


def test_encode_no_arguments():
    """Test error when no arguments provided."""
    result = run_util_command(["encode"])
    assert result.returncode != 0
    assert "required" in result.stderr.lower() or "error" in result.stderr.lower()
