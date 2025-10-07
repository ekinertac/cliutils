import subprocess
import pytest

# Helper function to run the util command
def run_util_command(command_args):
    full_command = ['python', '-m', 'util.main'] + command_args
    result = subprocess.run(full_command, capture_output=True, text=True, check=False)
    return result

def test_completion_bash_output():
    result = run_util_command(['completion', 'bash'])
    assert result.returncode == 0
    assert "To activate autocompletion for bash" in result.stdout
    assert "eval \"$(register-python-argcomplete util)\"" in result.stdout

def test_completion_zsh_output():
    result = run_util_command(['completion', 'zsh'])
    assert result.returncode == 0
    assert "To activate autocompletion for zsh" in result.stdout
    assert "eval \"$(register-python-argcomplete util)\"" in result.stdout

def test_completion_unsupported_shell_error():
    result = run_util_command(['completion', 'fish'])
    assert result.returncode != 0
    assert "argument shell: invalid choice: 'fish'" in result.stderr
