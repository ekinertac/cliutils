import subprocess


def run_util_command(args):
    """Helper function to run util command as a subprocess."""
    result = subprocess.run(
        ["python", "-m", "util.main"] + args,
        capture_output=True,
        text=True,
    )
    return result


def test_case_lower():
    result = run_util_command(["case", "lower", "HELLO WORLD"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello world"


def test_case_lower_mixed():
    result = run_util_command(["case", "lower", "HeLLo WoRLd"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello world"


def test_case_upper():
    result = run_util_command(["case", "upper", "hello world"])
    assert result.returncode == 0
    assert result.stdout.strip() == "HELLO WORLD"


def test_case_upper_mixed():
    result = run_util_command(["case", "upper", "HeLLo WoRLd"])
    assert result.returncode == 0
    assert result.stdout.strip() == "HELLO WORLD"


def test_case_camel_from_spaces():
    result = run_util_command(["case", "camel", "hello world"])
    assert result.returncode == 0
    assert result.stdout.strip() == "helloWorld"


def test_case_camel_from_snake():
    result = run_util_command(["case", "camel", "hello_world_test"])
    assert result.returncode == 0
    assert result.stdout.strip() == "helloWorldTest"


def test_case_camel_from_kebab():
    result = run_util_command(["case", "camel", "hello-world-test"])
    assert result.returncode == 0
    assert result.stdout.strip() == "helloWorldTest"


def test_case_pascal_from_spaces():
    result = run_util_command(["case", "pascal", "hello world"])
    assert result.returncode == 0
    assert result.stdout.strip() == "HelloWorld"


def test_case_pascal_from_snake():
    result = run_util_command(["case", "pascal", "hello_world_test"])
    assert result.returncode == 0
    assert result.stdout.strip() == "HelloWorldTest"


def test_case_snake_from_spaces():
    result = run_util_command(["case", "snake", "hello world"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello_world"


def test_case_snake_from_camel():
    result = run_util_command(["case", "snake", "helloWorld"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello_world"


def test_case_snake_from_pascal():
    result = run_util_command(["case", "snake", "HelloWorld"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello_world"


def test_case_snake_from_kebab():
    result = run_util_command(["case", "snake", "hello-world-test"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello_world_test"


def test_case_constant_from_spaces():
    result = run_util_command(["case", "constant", "hello world"])
    assert result.returncode == 0
    assert result.stdout.strip() == "HELLO_WORLD"


def test_case_constant_from_camel():
    result = run_util_command(["case", "constant", "helloWorld"])
    assert result.returncode == 0
    assert result.stdout.strip() == "HELLO_WORLD"


def test_case_constant_from_snake():
    result = run_util_command(["case", "constant", "hello_world"])
    assert result.returncode == 0
    assert result.stdout.strip() == "HELLO_WORLD"


def test_case_kebab_from_spaces():
    result = run_util_command(["case", "kebab", "hello world"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello-world"


def test_case_kebab_from_camel():
    result = run_util_command(["case", "kebab", "helloWorld"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello-world"


def test_case_kebab_from_snake():
    result = run_util_command(["case", "kebab", "hello_world"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello-world"


def test_case_header_from_spaces():
    result = run_util_command(["case", "header", "hello world"])
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello-World"


def test_case_header_from_snake():
    result = run_util_command(["case", "header", "hello_world_test"])
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello-World-Test"


def test_case_title_from_spaces():
    result = run_util_command(["case", "title", "hello world"])
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello World"


def test_case_title_from_snake():
    result = run_util_command(["case", "title", "hello_world_test"])
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello_World_Test"


def test_case_title_from_kebab():
    result = run_util_command(["case", "title", "hello-world-test"])
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello-World-Test"


def test_case_sentence():
    result = run_util_command(["case", "sentence", "HELLO WORLD"])
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello world"


def test_case_sentence_lowercase():
    result = run_util_command(["case", "sentence", "hello world"])
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello world"


def test_case_sentence_mixed():
    result = run_util_command(["case", "sentence", "hELLO wORLD"])
    assert result.returncode == 0
    assert result.stdout.strip() == "Hello world"


def test_case_empty_string():
    result = run_util_command(["case", "lower", ""])
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_case_single_word():
    result = run_util_command(["case", "snake", "Hello"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello"


def test_case_with_numbers():
    result = run_util_command(["case", "camel", "hello world 123"])
    assert result.returncode == 0
    assert result.stdout.strip() == "helloWorld123"


def test_case_snake_with_numbers():
    result = run_util_command(["case", "snake", "helloWorld123"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hello_world123"


def test_case_no_arguments():
    result = run_util_command(["case"])
    assert result.returncode != 0
    assert "required" in result.stderr.lower() or "error" in result.stderr.lower()


def test_case_help():
    result = run_util_command(["case", "--help"])
    assert result.returncode == 0
    assert "case" in result.stdout.lower()
    assert "camel" in result.stdout.lower()


def test_case_lower_help():
    result = run_util_command(["case", "lower", "--help"])
    assert result.returncode == 0
    assert "lower" in result.stdout.lower()


def test_case_camel_help():
    result = run_util_command(["case", "camel", "--help"])
    assert result.returncode == 0
    assert "camel" in result.stdout.lower()


def test_case_snake_help():
    result = run_util_command(["case", "snake", "--help"])
    assert result.returncode == 0
    assert "snake" in result.stdout.lower()
