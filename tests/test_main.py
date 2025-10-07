import subprocess
import pytest

# Helper function to run the util command
def run_util_command(command_args):
    full_command = ['python', '-m', 'util.main'] + command_args
    result = subprocess.run(full_command, capture_output=True, text=True, check=False)
    return result

def test_main_no_arguments_prints_help():
    result = run_util_command([])
    assert result.returncode != 0
    assert "usage: util" in result.stderr or "usage: util" in result.stdout
    assert "Available commands" in result.stderr or "Available commands" in result.stdout

def test_main_unknown_command_prints_error():
    result = run_util_command(['nonexistentcommand'])
    assert result.returncode != 0
    assert "invalid choice: 'nonexistentcommand'" in result.stderr

def test_main_help_flag_prints_help():
    result = run_util_command(['--help'])
    assert result.returncode == 0
    assert "usage: util" in result.stdout
    assert "Available commands" in result.stdout

def test_subcommand_help_flag_prints_help():
    result = run_util_command(['uuid', '--help'])
    assert result.returncode == 0
    assert "usage: util uuid" in result.stdout
    assert "Generate various types of Universally Unique Identifiers (UUIDs)." in result.stdout

def test_subcommand_version_help_flag_prints_help():
    result = run_util_command(['uuid', 'v1', '--help'])
    assert result.returncode == 0
    assert "usage: util uuid v1" in result.stdout
    assert "Generate a time-based UUID (version 1)." in result.stdout
