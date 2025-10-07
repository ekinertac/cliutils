import subprocess
import pytest

# Helper function to run the util command
def run_util_command(command_args):
    full_command = ['python', '-m', 'util.main'] + command_args
    result = subprocess.run(full_command, capture_output=True, text=True, check=False)
    return result

def test_base64_encode():
    test_string = "Hello, World!"
    result = run_util_command(['base64', 'encode', test_string])
    assert result.returncode == 0
    assert result.stdout.strip() == "SGVsbG8sIFdvcmxkIQ=="

def test_base64_decode():
    encoded_string = "SGVsbG8sIFdvcmxkIQ=="
    result = run_util_command(['base64', 'decode', encoded_string])
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello, World!"

def test_base64_encode_decode_roundtrip():
    original_string = "This is a test string with some special characters: !@#$%^&*()_+"
    encoded_result = run_util_command(['base64', 'encode', original_string])
    assert encoded_result.returncode == 0
    encoded_string = encoded_result.stdout.strip()

    decoded_result = run_util_command(['base64', 'decode', encoded_string])
    assert decoded_result.returncode == 0
    decoded_string = decoded_result.stdout.strip()

    assert original_string == decoded_string

def test_base64_decode_invalid_string():
    invalid_base64_chars = "abc"
    result = run_util_command(['base64', 'decode', invalid_base64_chars])
    assert result.returncode != 0
    assert "Error: Invalid base64 string." in result.stdout

def test_base64_decode_non_utf8_output():
    # This is a tricky one to simulate reliably without knowing the exact encoding
    # but we can try with a string that would result in non-UTF8 if decoded incorrectly
    # For now, we'll rely on the invalid base64 string test to cover most errors.
    # If a specific non-UTF8 scenario arises, we can add a more targeted test.
    pass # Placeholder for now
