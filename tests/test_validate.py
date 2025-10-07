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
# JSON VALIDATION TESTS
# ============================================================================


def test_validate_syntax_json_valid():
    """Test validating valid JSON."""
    result = run_util_command(["validate", "syntax", "json", '{"name": "test"}'])
    assert result.returncode == 0
    assert "Valid JSON" in result.stdout


def test_validate_syntax_json_invalid():
    """Test validating invalid JSON."""
    result = run_util_command(["validate", "syntax", "json", '{"name": test}'])
    assert result.returncode != 0
    assert "Invalid JSON" in result.stderr


def test_validate_syntax_json_from_file():
    """Test validating JSON from file (auto-detected)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        json_file = os.path.join(tmpdir, "test.json")
        with open(json_file, "w") as f:
            f.write('{"valid": true, "count": 42}')

        result = run_util_command(["validate", "syntax", "json", json_file])
        assert result.returncode == 0
        assert "Valid JSON" in result.stdout


# ============================================================================
# YAML VALIDATION TESTS
# ============================================================================


def test_validate_syntax_yaml_valid():
    """Test validating valid YAML."""
    result = run_util_command(["validate", "syntax", "yaml", "name: test\nage: 30"])
    assert result.returncode == 0
    assert "Valid YAML" in result.stdout


def test_validate_syntax_yaml_invalid():
    """Test validating invalid YAML."""
    result = run_util_command(
        ["validate", "syntax", "yaml", "name: test\n  invalid: indent"]
    )
    assert result.returncode != 0
    assert "Invalid YAML" in result.stderr


def test_validate_syntax_yaml_alias():
    """Test using yml alias."""
    result = run_util_command(["validate", "syntax", "yml", "key: value"])
    assert result.returncode == 0
    assert "Valid YML" in result.stdout


# ============================================================================
# TOML VALIDATION TESTS
# ============================================================================


def test_validate_syntax_toml_valid():
    """Test validating valid TOML."""
    toml_content = '[section]\nname = "test"\nvalue = 42'
    result = run_util_command(["validate", "syntax", "toml", toml_content])
    assert result.returncode == 0
    assert "Valid TOML" in result.stdout


def test_validate_syntax_toml_invalid():
    """Test validating invalid TOML."""
    result = run_util_command(["validate", "syntax", "toml", "invalid = "])
    assert result.returncode != 0
    assert "Invalid TOML" in result.stderr


# ============================================================================
# XML VALIDATION TESTS
# ============================================================================


def test_validate_syntax_xml_valid():
    """Test validating valid XML."""
    xml_content = '<?xml version="1.0"?><root><item>test</item></root>'
    result = run_util_command(["validate", "syntax", "xml", xml_content])
    assert result.returncode == 0
    assert "Valid XML" in result.stdout


def test_validate_syntax_xml_invalid():
    """Test validating invalid XML."""
    result = run_util_command(["validate", "syntax", "xml", "<root><item>test</root>"])
    assert result.returncode != 0
    assert "Invalid XML" in result.stderr


# ============================================================================
# HTML VALIDATION TESTS
# ============================================================================


def test_validate_syntax_html_valid():
    """Test validating valid HTML."""
    html_content = "<html><body><div>Test</div></body></html>"
    result = run_util_command(["validate", "syntax", "html", html_content])
    assert result.returncode == 0
    assert "Valid HTML" in result.stdout


def test_validate_syntax_html_self_closing():
    """Test HTML with self-closing tags."""
    html_content = "<html><body><br><img src='test.jpg'></body></html>"
    result = run_util_command(["validate", "syntax", "html", html_content])
    assert result.returncode == 0
    assert "Valid HTML" in result.stdout


def test_validate_syntax_html_mismatched():
    """Test HTML with mismatched tags."""
    html_content = "<html><body><div>Test</span></body></html>"
    result = run_util_command(["validate", "syntax", "html", html_content])
    assert result.returncode != 0
    assert "Invalid HTML" in result.stderr


def test_validate_syntax_html_unclosed():
    """Test HTML with unclosed tags."""
    html_content = "<html><body><div>Test</body></html>"
    result = run_util_command(["validate", "syntax", "html", html_content])
    assert result.returncode != 0
    assert "Unclosed" in result.stderr or "Mismatched" in result.stderr


# ============================================================================
# CSS VALIDATION TESTS
# ============================================================================


def test_validate_syntax_css_valid():
    """Test validating valid CSS."""
    css_content = "body { color: red; } .class { margin: 10px; }"
    result = run_util_command(["validate", "syntax", "css", css_content])
    assert result.returncode == 0
    assert "Valid CSS" in result.stdout


def test_validate_syntax_css_unmatched_brace():
    """Test CSS with unmatched braces."""
    css_content = "body { color: red; "
    result = run_util_command(["validate", "syntax", "css", css_content])
    assert result.returncode != 0
    assert "Unclosed" in result.stderr or "Invalid CSS" in result.stderr


def test_validate_syntax_css_unmatched_paren():
    """Test CSS with unmatched parentheses."""
    css_content = "body { background: rgb(255, 0, 0; }"
    result = run_util_command(["validate", "syntax", "css", css_content])
    assert result.returncode != 0
    assert "Invalid CSS" in result.stderr


# ============================================================================
# EMAIL VALIDATION TESTS
# ============================================================================


def test_validate_email_valid():
    """Test validating valid email."""
    result = run_util_command(["validate", "email", "test@example.com"])
    assert result.returncode == 0
    assert "Valid email" in result.stdout


def test_validate_email_valid_complex():
    """Test validating complex valid email."""
    result = run_util_command(["validate", "email", "user.name+tag@example.co.uk"])
    assert result.returncode == 0
    assert "Valid email" in result.stdout


def test_validate_email_invalid_no_at():
    """Test email without @ symbol."""
    result = run_util_command(["validate", "email", "testexample.com"])
    assert result.returncode != 0
    assert "Invalid email" in result.stderr


def test_validate_email_invalid_no_domain():
    """Test email without domain."""
    result = run_util_command(["validate", "email", "test@"])
    assert result.returncode != 0
    assert "Invalid email" in result.stderr


# ============================================================================
# URL VALIDATION TESTS
# ============================================================================


def test_validate_url_http():
    """Test validating HTTP URL."""
    result = run_util_command(["validate", "url", "http://example.com"])
    assert result.returncode == 0
    assert "Valid URL" in result.stdout


def test_validate_url_https():
    """Test validating HTTPS URL."""
    result = run_util_command(["validate", "url", "https://example.com/path/to/page"])
    assert result.returncode == 0
    assert "Valid URL" in result.stdout


def test_validate_url_with_port():
    """Test URL with port."""
    result = run_util_command(["validate", "url", "http://localhost:8080"])
    assert result.returncode == 0
    assert "Valid URL" in result.stdout


def test_validate_url_invalid_no_protocol():
    """Test URL without protocol."""
    result = run_util_command(["validate", "url", "example.com"])
    assert result.returncode != 0
    assert "Invalid URL" in result.stderr


def test_validate_url_invalid_format():
    """Test invalid URL format."""
    result = run_util_command(["validate", "url", "htp://invalid"])
    assert result.returncode != 0
    assert "Invalid URL" in result.stderr


# ============================================================================
# IP ADDRESS VALIDATION TESTS
# ============================================================================


def test_validate_ip_ipv4_valid():
    """Test validating valid IPv4."""
    result = run_util_command(["validate", "ip", "192.168.1.1"])
    assert result.returncode == 0
    assert "Valid IPv4" in result.stdout


def test_validate_ip_ipv4_explicit():
    """Test validating IPv4 with explicit version."""
    result = run_util_command(["validate", "ip", "10.0.0.1", "--version", "4"])
    assert result.returncode == 0
    assert "Valid IPv4" in result.stdout


def test_validate_ip_ipv4_invalid_octet():
    """Test IPv4 with invalid octet."""
    result = run_util_command(["validate", "ip", "192.168.1.256", "--version", "4"])
    assert result.returncode != 0
    assert "Invalid IPv4" in result.stderr


def test_validate_ip_ipv6_valid():
    """Test validating valid IPv6."""
    result = run_util_command(
        ["validate", "ip", "2001:0db8:85a3:0000:0000:8a2e:0370:7334"]
    )
    assert result.returncode == 0
    assert "Valid IPv6" in result.stdout


def test_validate_ip_ipv6_short():
    """Test validating short IPv6."""
    result = run_util_command(["validate", "ip", "2001:db8::1"])
    assert result.returncode == 0
    assert "Valid IPv6" in result.stdout


def test_validate_ip_ipv6_loopback():
    """Test validating IPv6 loopback."""
    result = run_util_command(["validate", "ip", "::1", "--version", "6"])
    assert result.returncode == 0
    assert "Valid IPv6" in result.stdout


def test_validate_ip_invalid():
    """Test validating invalid IP."""
    result = run_util_command(["validate", "ip", "not.an.ip.address"])
    assert result.returncode != 0
    assert "Invalid" in result.stderr


# ============================================================================
# CREDIT CARD VALIDATION TESTS
# ============================================================================


def test_validate_card_valid_visa():
    """Test validating valid Visa card."""
    result = run_util_command(["validate", "card", "4532015112830366"])
    assert result.returncode == 0
    assert "Valid credit card" in result.stdout


def test_validate_card_valid_mastercard():
    """Test validating valid Mastercard."""
    result = run_util_command(["validate", "card", "5425233430109903"])
    assert result.returncode == 0
    assert "Valid credit card" in result.stdout


def test_validate_card_with_spaces():
    """Test credit card with spaces."""
    result = run_util_command(["validate", "card", "4532 0151 1283 0366"])
    assert result.returncode == 0
    assert "Valid credit card" in result.stdout


def test_validate_card_with_hyphens():
    """Test credit card with hyphens."""
    result = run_util_command(["validate", "card", "5425-2334-3010-9903"])
    assert result.returncode == 0
    assert "Valid credit card" in result.stdout


def test_validate_card_invalid_luhn():
    """Test credit card that fails Luhn check."""
    result = run_util_command(["validate", "card", "4532015112830367"])
    assert result.returncode != 0
    assert "Luhn check failed" in result.stderr


def test_validate_card_invalid_length():
    """Test credit card with invalid length."""
    result = run_util_command(["validate", "card", "123456"])
    assert result.returncode != 0
    assert "13-19 digits" in result.stderr


def test_validate_card_alias_cc():
    """Test using cc alias."""
    result = run_util_command(["validate", "cc", "4532015112830366"])
    assert result.returncode == 0
    assert "Valid credit card" in result.stdout


def test_validate_card_alias_credit_card():
    """Test using credit-card alias."""
    result = run_util_command(["validate", "credit-card", "5425233430109903"])
    assert result.returncode == 0
    assert "Valid credit card" in result.stdout


# ============================================================================
# CHECKSUM VALIDATION TESTS
# ============================================================================


def test_validate_checksum_sha256():
    """Test validating file checksum with SHA256."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Hello, World!")

        # Calculate expected checksum
        import hashlib

        with open(test_file, "rb") as f:
            expected = hashlib.sha256(f.read()).hexdigest()

        result = run_util_command(["validate", "checksum", test_file, expected])
        assert result.returncode == 0
        assert "Checksum verified" in result.stdout


def test_validate_checksum_md5():
    """Test validating file checksum with MD5."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Test content")

        import hashlib

        with open(test_file, "rb") as f:
            expected = hashlib.md5(f.read()).hexdigest()

        result = run_util_command(
            ["validate", "checksum", test_file, expected, "--algorithm", "md5"]
        )
        assert result.returncode == 0
        assert "Checksum verified" in result.stdout


def test_validate_checksum_mismatch():
    """Test checksum validation with mismatched hash."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Content")

        wrong_hash = "0" * 64
        result = run_util_command(["validate", "checksum", test_file, wrong_hash])
        assert result.returncode != 0
        assert "Checksum mismatch" in result.stderr


def test_validate_checksum_file_not_found():
    """Test checksum validation with non-existent file."""
    result = run_util_command(
        ["validate", "checksum", "/tmp/nonexistent.txt", "abc123"]
    )
    assert result.returncode != 0
    assert "File not found" in result.stderr


def test_validate_checksum_alias_hash():
    """Test using hash alias."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, "w") as f:
            f.write("Test")

        import hashlib

        with open(test_file, "rb") as f:
            expected = hashlib.sha256(f.read()).hexdigest()

        result = run_util_command(["validate", "hash", test_file, expected])
        assert result.returncode == 0
        assert "Checksum verified" in result.stdout


# ============================================================================
# HELP TESTS
# ============================================================================


def test_validate_help():
    """Test validate command help."""
    result = run_util_command(["validate", "--help"])
    assert result.returncode == 0
    assert "validate" in result.stdout.lower()


def test_validate_syntax_help():
    """Test syntax validation help."""
    result = run_util_command(["validate", "syntax", "--help"])
    assert result.returncode == 0
    assert "syntax" in result.stdout.lower()


def test_validate_no_arguments():
    """Test error when no arguments provided."""
    result = run_util_command(["validate"])
    assert result.returncode != 0
    assert "required" in result.stderr.lower() or "error" in result.stderr.lower()


# ============================================================================
# UUID VALIDATION TESTS
# ============================================================================


def test_validate_uuid_v4():
    """Test validating UUID v4."""
    result = run_util_command(
        ["validate", "uuid", "550e8400-e29b-41d4-a716-446655440000"]
    )
    assert result.returncode == 0
    assert "Valid UUID v4" in result.stdout


def test_validate_uuid_v1():
    """Test validating UUID v1."""
    result = run_util_command(
        ["validate", "uuid", "c232ab00-9414-11ec-b3c8-9f6bdeced846"]
    )
    assert result.returncode == 0
    assert "Valid UUID v1" in result.stdout


def test_validate_uuid_invalid():
    """Test invalid UUID."""
    result = run_util_command(["validate", "uuid", "not-a-uuid"])
    assert result.returncode != 0
    assert "Invalid UUID" in result.stderr


def test_validate_uuid_invalid_version():
    """Test UUID with invalid version."""
    result = run_util_command(
        ["validate", "uuid", "550e8400-e29b-91d4-a716-446655440000"]
    )
    assert result.returncode != 0
    assert "Invalid UUID" in result.stderr


# ============================================================================
# BASE64 VALIDATION TESTS
# ============================================================================


def test_validate_base64_valid():
    """Test validating valid base64."""
    result = run_util_command(["validate", "base64", "SGVsbG8gV29ybGQ="])
    assert result.returncode == 0
    assert "Valid base64" in result.stdout


def test_validate_base64_valid_no_padding():
    """Test base64 without padding."""
    result = run_util_command(["validate", "base64", "SGVsbG8gV29ybGQ"])
    assert result.returncode == 0
    assert "Valid base64" in result.stdout


def test_validate_base64_invalid_chars():
    """Test base64 with invalid characters."""
    result = run_util_command(["validate", "base64", "Hello@World!"])
    assert result.returncode != 0
    assert "Invalid base64" in result.stderr


def test_validate_base64_alias():
    """Test using b64 alias."""
    result = run_util_command(["validate", "b64", "dGVzdA=="])
    assert result.returncode == 0
    assert "Valid base64" in result.stdout


# ============================================================================
# DATE VALIDATION TESTS
# ============================================================================


def test_validate_date_iso8601_date_only():
    """Test ISO 8601 date only format."""
    result = run_util_command(["validate", "date", "2024-01-15"])
    assert result.returncode == 0
    assert "Valid ISO 8601 date" in result.stdout


def test_validate_date_iso8601_datetime():
    """Test ISO 8601 datetime format."""
    result = run_util_command(["validate", "date", "2024-01-15T10:30:00"])
    assert result.returncode == 0
    assert "Valid ISO 8601 date" in result.stdout


def test_validate_date_iso8601_with_z():
    """Test ISO 8601 datetime with Z timezone."""
    result = run_util_command(["validate", "date", "2024-01-15T10:30:00Z"])
    assert result.returncode == 0
    assert "Valid ISO 8601 date" in result.stdout


def test_validate_date_iso8601_with_offset():
    """Test ISO 8601 datetime with timezone offset."""
    result = run_util_command(["validate", "date", "2024-01-15T10:30:00+05:30"])
    assert result.returncode == 0
    assert "Valid ISO 8601 date" in result.stdout


def test_validate_date_iso8601_with_microseconds():
    """Test ISO 8601 datetime with microseconds."""
    result = run_util_command(["validate", "date", "2024-01-15T10:30:00.123456Z"])
    assert result.returncode == 0
    assert "Valid ISO 8601 date" in result.stdout


def test_validate_date_invalid():
    """Test invalid date format."""
    result = run_util_command(["validate", "date", "15/01/2024"])
    assert result.returncode != 0
    assert "Invalid" in result.stderr


def test_validate_date_alias():
    """Test using iso8601 alias."""
    result = run_util_command(["validate", "iso8601", "2024-01-15"])
    assert result.returncode == 0
    assert "Valid ISO 8601 date" in result.stdout


# ============================================================================
# PASSWORD STRENGTH TESTS
# ============================================================================


def test_validate_password_strong():
    """Test strong password."""
    result = run_util_command(["validate", "password", "MyP@ssw0rd123!"])
    assert result.returncode == 0
    assert "strong" in result.stdout.lower()


def test_validate_password_weak_short():
    """Test weak password (too short)."""
    result = run_util_command(["validate", "password", "Test1!"])
    assert result.returncode != 0
    assert "too short" in result.stderr


def test_validate_password_weak_no_uppercase():
    """Test password without uppercase."""
    result = run_util_command(["validate", "password", "test1234!"])
    assert result.returncode != 0
    assert "no uppercase" in result.stderr


def test_validate_password_weak_no_special():
    """Test password without special characters."""
    result = run_util_command(["validate", "password", "Test1234"])
    assert result.returncode != 0
    assert "no special" in result.stderr


def test_validate_password_common_pattern():
    """Test password with common pattern."""
    result = run_util_command(["validate", "password", "Password123!"])
    assert result.returncode != 0
    assert "common pattern" in result.stderr


def test_validate_password_alias_pwd():
    """Test using pwd alias."""
    result = run_util_command(["validate", "pwd", "MySecure123!"])
    assert result.returncode == 0


def test_validate_password_alias_pass():
    """Test using pass alias."""
    result = run_util_command(["validate", "pass", "AnotherGood1!"])
    assert result.returncode == 0


# ============================================================================
# REGEX VALIDATION TESTS
# ============================================================================


def test_validate_regex_valid_simple():
    """Test valid simple regex."""
    result = run_util_command(["validate", "regex", "^[a-z]+$"])
    assert result.returncode == 0
    assert "Valid regex" in result.stdout


def test_validate_regex_valid_complex():
    """Test valid complex regex."""
    result = run_util_command(
        ["validate", "regex", r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"]
    )
    assert result.returncode == 0
    assert "Valid regex" in result.stdout


def test_validate_regex_invalid_unclosed_bracket():
    """Test regex with unclosed bracket."""
    result = run_util_command(["validate", "regex", "^[unclosed"])
    assert result.returncode != 0
    assert "Invalid regex" in result.stderr


def test_validate_regex_invalid_unclosed_paren():
    """Test regex with unclosed parenthesis."""
    result = run_util_command(["validate", "regex", "^(test"])
    assert result.returncode != 0
    assert "Invalid regex" in result.stderr


def test_validate_regex_alias():
    """Test using regexp alias."""
    result = run_util_command(["validate", "regexp", "\\d+"])
    assert result.returncode == 0
    assert "Valid regex" in result.stdout


# ============================================================================
# CRON VALIDATION TESTS
# ============================================================================


def test_validate_cron_every_hour():
    """Test valid cron expression (every hour)."""
    result = run_util_command(["validate", "cron", "0 * * * *"])
    assert result.returncode == 0
    assert "Valid cron" in result.stdout


def test_validate_cron_every_two_hours():
    """Test valid cron expression (every 2 hours)."""
    result = run_util_command(["validate", "cron", "0 */2 * * *"])
    assert result.returncode == 0
    assert "Valid cron" in result.stdout


def test_validate_cron_specific_time():
    """Test cron expression with specific time."""
    result = run_util_command(["validate", "cron", "30 14 * * 1"])
    assert result.returncode == 0
    assert "Valid cron" in result.stdout


def test_validate_cron_with_ranges():
    """Test cron expression with ranges."""
    result = run_util_command(["validate", "cron", "0 9-17 * * 1-5"])
    assert result.returncode == 0
    assert "Valid cron" in result.stdout


def test_validate_cron_with_lists():
    """Test cron expression with lists."""
    result = run_util_command(["validate", "cron", "0 0,12 * * *"])
    assert result.returncode == 0
    assert "Valid cron" in result.stdout


def test_validate_cron_six_fields():
    """Test cron expression with 6 fields (including seconds)."""
    result = run_util_command(["validate", "cron", "0 0 * * * *"])
    assert result.returncode == 0
    assert "Valid cron" in result.stdout


def test_validate_cron_invalid_too_few_fields():
    """Test cron with too few fields."""
    result = run_util_command(["validate", "cron", "0 * * *"])
    assert result.returncode != 0
    assert "Expected 5 or 6 fields" in result.stderr


def test_validate_cron_invalid_minute():
    """Test cron with invalid minute."""
    result = run_util_command(["validate", "cron", "99 * * * *"])
    assert result.returncode != 0
    assert "Invalid" in result.stderr


def test_validate_cron_invalid_hour():
    """Test cron with invalid hour."""
    result = run_util_command(["validate", "cron", "0 25 * * *"])
    assert result.returncode != 0
    assert "Invalid" in result.stderr
