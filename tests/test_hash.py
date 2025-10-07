import hashlib
import subprocess


def run_util_command(args):
    """Helper function to run util command as a subprocess."""
    result = subprocess.run(
        ["python", "-m", "util.main"] + args,
        capture_output=True,
        text=True,
    )
    return result


def test_hash_md5():
    test_string = "Hello, World!"
    result = run_util_command(["hash", "md5", test_string])
    assert result.returncode == 0
    expected_hash = hashlib.md5(test_string.encode("utf-8")).hexdigest()
    assert result.stdout.strip() == expected_hash


def test_hash_sha1():
    test_string = "Hello, World!"
    result = run_util_command(["hash", "sha1", test_string])
    assert result.returncode == 0
    expected_hash = hashlib.sha1(test_string.encode("utf-8")).hexdigest()
    assert result.stdout.strip() == expected_hash


def test_hash_sha224():
    test_string = "Hello, World!"
    result = run_util_command(["hash", "sha224", test_string])
    assert result.returncode == 0
    expected_hash = hashlib.sha224(test_string.encode("utf-8")).hexdigest()
    assert result.stdout.strip() == expected_hash


def test_hash_sha256():
    test_string = "Hello, World!"
    result = run_util_command(["hash", "sha256", test_string])
    assert result.returncode == 0
    expected_hash = hashlib.sha256(test_string.encode("utf-8")).hexdigest()
    assert result.stdout.strip() == expected_hash


def test_hash_sha384():
    test_string = "Hello, World!"
    result = run_util_command(["hash", "sha384", test_string])
    assert result.returncode == 0
    expected_hash = hashlib.sha384(test_string.encode("utf-8")).hexdigest()
    assert result.stdout.strip() == expected_hash


def test_hash_sha512():
    test_string = "Hello, World!"
    result = run_util_command(["hash", "sha512", test_string])
    assert result.returncode == 0
    expected_hash = hashlib.sha512(test_string.encode("utf-8")).hexdigest()
    assert result.stdout.strip() == expected_hash


def test_hash_empty_string():
    test_string = ""
    result = run_util_command(["hash", "sha256", test_string])
    assert result.returncode == 0
    expected_hash = hashlib.sha256(test_string.encode("utf-8")).hexdigest()
    assert result.stdout.strip() == expected_hash


def test_hash_special_characters():
    test_string = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
    result = run_util_command(["hash", "sha256", test_string])
    assert result.returncode == 0
    expected_hash = hashlib.sha256(test_string.encode("utf-8")).hexdigest()
    assert result.stdout.strip() == expected_hash


def test_hash_unicode():
    test_string = "Hello, 世界!"
    result = run_util_command(["hash", "sha256", test_string])
    assert result.returncode == 0
    expected_hash = hashlib.sha256(test_string.encode("utf-8")).hexdigest()
    assert result.stdout.strip() == expected_hash


def test_hash_multiline():
    test_string = "Line 1\nLine 2\nLine 3"
    result = run_util_command(["hash", "sha256", test_string])
    assert result.returncode == 0
    expected_hash = hashlib.sha256(test_string.encode("utf-8")).hexdigest()
    assert result.stdout.strip() == expected_hash


def test_hash_no_arguments():
    result = run_util_command(["hash"])
    assert result.returncode != 0
    assert "required" in result.stderr.lower() or "error" in result.stderr.lower()


def test_hash_help():
    result = run_util_command(["hash", "--help"])
    assert result.returncode == 0
    assert "hash" in result.stdout.lower()
    assert "md5" in result.stdout.lower()


def test_hash_md5_help():
    result = run_util_command(["hash", "md5", "--help"])
    assert result.returncode == 0
    assert "md5" in result.stdout.lower()
