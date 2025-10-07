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


def test_random_int_default():
    result = run_util_command(["random", "int"])
    assert result.returncode == 0
    value = int(result.stdout.strip())
    # Default range is 0-100
    assert 0 <= value <= 100


def test_random_int_custom_range():
    result = run_util_command(["random", "int", "--min", "10", "--max", "20"])
    assert result.returncode == 0
    value = int(result.stdout.strip())
    assert 10 <= value <= 20


def test_random_int_negative_range():
    result = run_util_command(["random", "int", "--min", "-50", "--max", "-10"])
    assert result.returncode == 0
    value = int(result.stdout.strip())
    assert -50 <= value <= -10


def test_random_int_single_value():
    result = run_util_command(["random", "int", "--min", "42", "--max", "42"])
    assert result.returncode == 0
    value = int(result.stdout.strip())
    assert value == 42


def test_random_int_invalid_range():
    result = run_util_command(["random", "int", "--min", "100", "--max", "50"])
    assert result.returncode != 0
    assert "error" in result.stderr.lower()


def test_random_int_alias():
    result = run_util_command(["random", "integer", "--min", "1", "--max", "10"])
    assert result.returncode == 0
    value = int(result.stdout.strip())
    assert 1 <= value <= 10


def test_random_float_default():
    result = run_util_command(["random", "float"])
    assert result.returncode == 0
    value = float(result.stdout.strip())
    # Default range is 0.0-1.0
    assert 0.0 <= value <= 1.0


def test_random_float_custom_range():
    result = run_util_command(["random", "float", "--min", "5.5", "--max", "10.5"])
    assert result.returncode == 0
    value = float(result.stdout.strip())
    assert 5.5 <= value <= 10.5


def test_random_float_negative_range():
    result = run_util_command(["random", "float", "--min", "-1.5", "--max", "-0.5"])
    assert result.returncode == 0
    value = float(result.stdout.strip())
    assert -1.5 <= value <= -0.5


def test_random_float_invalid_range():
    result = run_util_command(["random", "float", "--min", "10.0", "--max", "5.0"])
    assert result.returncode != 0
    assert "error" in result.stderr.lower()


def test_random_string_default():
    result = run_util_command(["random", "string"])
    assert result.returncode == 0
    text = result.stdout.strip()
    # Default length is 10, contains letters and digits
    assert len(text) == 10
    assert re.match(r"^[A-Za-z0-9]+$", text)


def test_random_string_custom_length():
    result = run_util_command(["random", "string", "--length", "25"])
    assert result.returncode == 0
    text = result.stdout.strip()
    assert len(text) == 25


def test_random_string_letters_only():
    result = run_util_command(["random", "string", "--length", "20", "--letters"])
    assert result.returncode == 0
    text = result.stdout.strip()
    assert len(text) == 20
    assert re.match(r"^[A-Za-z]+$", text)


def test_random_string_digits_only():
    result = run_util_command(["random", "string", "--length", "15", "--digits"])
    assert result.returncode == 0
    text = result.stdout.strip()
    assert len(text) == 15
    assert re.match(r"^[0-9]+$", text)


def test_random_string_letters_and_digits():
    result = run_util_command(
        ["random", "string", "--length", "30", "--letters", "--digits"]
    )
    assert result.returncode == 0
    text = result.stdout.strip()
    assert len(text) == 30
    assert re.match(r"^[A-Za-z0-9]+$", text)


def test_random_string_with_punctuation():
    result = run_util_command(
        ["random", "string", "--length", "20", "--letters", "--digits", "--punctuation"]
    )
    assert result.returncode == 0
    text = result.stdout.strip()
    assert len(text) == 20
    # Should contain letters, digits, and/or punctuation


def test_random_string_lowercase():
    result = run_util_command(["random", "string", "--length", "15", "--lowercase"])
    assert result.returncode == 0
    text = result.stdout.strip()
    assert len(text) == 15
    assert re.match(r"^[a-z]+$", text)


def test_random_string_uppercase():
    result = run_util_command(["random", "string", "--length", "15", "--uppercase"])
    assert result.returncode == 0
    text = result.stdout.strip()
    assert len(text) == 15
    assert re.match(r"^[A-Z]+$", text)


def test_random_string_lowercase_with_digits():
    result = run_util_command(
        ["random", "string", "--length", "20", "--lowercase", "--digits"]
    )
    assert result.returncode == 0
    text = result.stdout.strip()
    assert len(text) == 20
    assert re.match(r"^[a-z0-9]+$", text)


def test_random_string_alias():
    result = run_util_command(["random", "str", "--length", "12"])
    assert result.returncode == 0
    text = result.stdout.strip()
    assert len(text) == 12


def test_random_choice():
    result = run_util_command(["random", "choice", "apple", "banana", "cherry"])
    assert result.returncode == 0
    choice = result.stdout.strip()
    assert choice in ["apple", "banana", "cherry"]


def test_random_choice_single_item():
    result = run_util_command(["random", "choice", "only-option"])
    assert result.returncode == 0
    choice = result.stdout.strip()
    assert choice == "only-option"


def test_random_choice_numbers():
    result = run_util_command(["random", "choice", "1", "2", "3", "4", "5"])
    assert result.returncode == 0
    choice = result.stdout.strip()
    assert choice in ["1", "2", "3", "4", "5"]


def test_random_shuffle():
    result = run_util_command(["random", "shuffle", "a", "b", "c", "d", "e"])
    assert result.returncode == 0
    shuffled = result.stdout.strip().split()
    # Should have all original items
    assert len(shuffled) == 5
    assert set(shuffled) == {"a", "b", "c", "d", "e"}


def test_random_shuffle_single_item():
    result = run_util_command(["random", "shuffle", "single"])
    assert result.returncode == 0
    shuffled = result.stdout.strip()
    assert shuffled == "single"


def test_random_shuffle_numbers():
    result = run_util_command(["random", "shuffle", "1", "2", "3", "4", "5", "6"])
    assert result.returncode == 0
    shuffled = result.stdout.strip().split()
    assert len(shuffled) == 6
    assert set(shuffled) == {"1", "2", "3", "4", "5", "6"}


def test_random_no_arguments():
    result = run_util_command(["random"])
    assert result.returncode != 0
    assert "required" in result.stderr.lower() or "error" in result.stderr.lower()


def test_random_help():
    result = run_util_command(["random", "--help"])
    assert result.returncode == 0
    assert "random" in result.stdout.lower()
    assert "int" in result.stdout.lower()


def test_random_int_help():
    result = run_util_command(["random", "int", "--help"])
    assert result.returncode == 0
    assert "int" in result.stdout.lower()


def test_random_string_help():
    result = run_util_command(["random", "string", "--help"])
    assert result.returncode == 0
    assert "string" in result.stdout.lower()


def test_random_choice_help():
    result = run_util_command(["random", "choice", "--help"])
    assert result.returncode == 0
    assert "choice" in result.stdout.lower()
