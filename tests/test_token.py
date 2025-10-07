import re
import subprocess


def run_util_command(args):
    """Helper function to run util command as a subprocess."""
    result = subprocess.run(
        ["python", "-m", "util.main"] + args,
        capture_output=True,
        text=True,
    )
    return result


def test_token_hex_default():
    result = run_util_command(["token", "hex"])
    assert result.returncode == 0
    token = result.stdout.strip()
    # Default is 32 bytes = 64 hex characters
    assert len(token) == 64
    assert re.match(r"^[0-9a-f]+$", token)


def test_token_hex_custom_bytes():
    result = run_util_command(["token", "hex", "--bytes", "16"])
    assert result.returncode == 0
    token = result.stdout.strip()
    # 16 bytes = 32 hex characters
    assert len(token) == 32
    assert re.match(r"^[0-9a-f]+$", token)


def test_token_hex_small():
    result = run_util_command(["token", "hex", "--bytes", "4"])
    assert result.returncode == 0
    token = result.stdout.strip()
    # 4 bytes = 8 hex characters
    assert len(token) == 8
    assert re.match(r"^[0-9a-f]+$", token)


def test_token_urlsafe_default():
    result = run_util_command(["token", "urlsafe"])
    assert result.returncode == 0
    token = result.stdout.strip()
    # URL-safe base64, should be alphanumeric with - and _
    assert len(token) > 0
    assert re.match(r"^[A-Za-z0-9_-]+$", token)


def test_token_urlsafe_custom_bytes():
    result = run_util_command(["token", "urlsafe", "--bytes", "24"])
    assert result.returncode == 0
    token = result.stdout.strip()
    assert len(token) > 0
    assert re.match(r"^[A-Za-z0-9_-]+$", token)


def test_token_bytes_default():
    result = run_util_command(["token", "bytes"])
    assert result.returncode == 0
    token = result.stdout.strip()
    # Default is 32 bytes = 64 hex characters
    assert len(token) == 64
    assert re.match(r"^[0-9a-f]+$", token)


def test_token_bytes_custom():
    result = run_util_command(["token", "bytes", "--bytes", "8"])
    assert result.returncode == 0
    token = result.stdout.strip()
    # 8 bytes = 16 hex characters
    assert len(token) == 16
    assert re.match(r"^[0-9a-f]+$", token)


def test_token_password_default():
    result = run_util_command(["token", "password"])
    assert result.returncode == 0
    password = result.stdout.strip()
    # Default length is 16
    assert len(password) == 16
    # Should contain only letters and digits (no special chars by default)
    assert re.match(r"^[A-Za-z0-9]+$", password)


def test_token_password_custom_length():
    result = run_util_command(["token", "password", "--length", "32"])
    assert result.returncode == 0
    password = result.stdout.strip()
    assert len(password) == 32
    assert re.match(r"^[A-Za-z0-9]+$", password)


def test_token_password_short():
    result = run_util_command(["token", "password", "--length", "8"])
    assert result.returncode == 0
    password = result.stdout.strip()
    assert len(password) == 8
    assert re.match(r"^[A-Za-z0-9]+$", password)


def test_token_password_with_special():
    result = run_util_command(["token", "password", "--length", "20", "--special"])
    assert result.returncode == 0
    password = result.stdout.strip()
    assert len(password) == 20
    # Should contain letters, digits, and possibly special characters
    # We can't guarantee special chars will appear in every generation,
    # but the format should allow them
    assert re.match(r"^[A-Za-z0-9!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~]+$", password)


def test_token_password_alias_pwd():
    result = run_util_command(["token", "pwd", "--length", "12"])
    assert result.returncode == 0
    password = result.stdout.strip()
    assert len(password) == 12


def test_token_password_alias_pass():
    result = run_util_command(["token", "pass", "--length", "10"])
    assert result.returncode == 0
    password = result.stdout.strip()
    assert len(password) == 10


def test_token_no_arguments():
    result = run_util_command(["token"])
    assert result.returncode != 0
    assert "required" in result.stderr.lower() or "error" in result.stderr.lower()


def test_token_help():
    result = run_util_command(["token", "--help"])
    assert result.returncode == 0
    assert "token" in result.stdout.lower()
    assert "hex" in result.stdout.lower()


def test_token_hex_help():
    result = run_util_command(["token", "hex", "--help"])
    assert result.returncode == 0
    assert "hex" in result.stdout.lower()


def test_token_password_help():
    result = run_util_command(["token", "password", "--help"])
    assert result.returncode == 0
    assert "password" in result.stdout.lower()


def test_token_uniqueness():
    # Generate two tokens and ensure they are different
    result1 = run_util_command(["token", "hex"])
    result2 = run_util_command(["token", "hex"])
    assert result1.returncode == 0
    assert result2.returncode == 0
    token1 = result1.stdout.strip()
    token2 = result2.stdout.strip()
    assert token1 != token2  # Should be cryptographically random
