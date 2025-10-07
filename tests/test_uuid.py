import subprocess
import json
import uuid
import pytest

# Helper function to run the util command
def run_util_command(command_args):
    # Prepend 'python -m util.main' to run the command
    # This is more reliable for testing than relying on the 'util' executable directly
    # as it bypasses potential PATH issues during testing.
    full_command = ['python', '-m', 'util.main'] + command_args
    result = subprocess.run(full_command, capture_output=True, text=True, check=False)
    return result

def test_uuid_default_v4():
    result = run_util_command(['uuid'])
    assert result.returncode == 0
    generated_uuid = result.stdout.strip()
    assert len(generated_uuid) == 36 # Standard UUID length
    # Attempt to parse as UUID to confirm validity
    assert uuid.UUID(generated_uuid).version == 4

def test_uuid_v1():
    result = run_util_command(['uuid', 'v1'])
    assert result.returncode == 0
    generated_uuid = result.stdout.strip()
    assert uuid.UUID(generated_uuid).version == 1

def test_uuid_v4_explicit():
    result = run_util_command(['uuid', 'v4'])
    assert result.returncode == 0
    generated_uuid = result.stdout.strip()
    assert uuid.UUID(generated_uuid).version == 4

def test_uuid_v3_valid():
    name = "testname"
    namespace = "6ba7b810-9dad-11d1-80b4-00c04fd430c8" # Example valid namespace UUID
    result = run_util_command(['uuid', 'v3', '--name', name, '--namespace', namespace])
    assert result.returncode == 0
    generated_uuid = result.stdout.strip()
    assert uuid.UUID(generated_uuid).version == 3
    # Verify it's the correct UUID for the given name and namespace
    expected_uuid = uuid.uuid3(uuid.UUID(namespace), name)
    assert str(expected_uuid) == generated_uuid

def test_uuid_v5_valid():
    name = "anothername"
    namespace = "6ba7b810-9dad-11d1-80b4-00c04fd430c8" # Example valid namespace UUID
    result = run_util_command(['uuid', 'v5', '--name', name, '--namespace', namespace])
    assert result.returncode == 0
    generated_uuid = result.stdout.strip()
    assert uuid.UUID(generated_uuid).version == 5
    # Verify it's the correct UUID for the given name and namespace
    expected_uuid = uuid.uuid5(uuid.UUID(namespace), name)
    assert str(expected_uuid) == generated_uuid

def test_uuid_v3_missing_name():
    namespace = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
    result = run_util_command(['uuid', 'v3', '--namespace', namespace])
    assert result.returncode != 0
    assert "the following arguments are required: --name" in result.stderr

def test_uuid_v3_missing_namespace():
    name = "testname"
    result = run_util_command(['uuid', 'v3', '--name', name])
    assert result.returncode != 0
    assert "the following arguments are required: --namespace" in result.stderr

def test_uuid_v3_invalid_namespace():
    name = "testname"
    invalid_namespace = "not-a-uuid"
    result = run_util_command(['uuid', 'v3', '--name', name, '--namespace', invalid_namespace])
    assert result.returncode != 0
    assert f"Error: Invalid namespace UUID '{invalid_namespace}'" in result.stdout # stdout because we print the error in the command itself

def test_uuid_v5_missing_name():
    namespace = "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
    result = run_util_command(['uuid', 'v5', '--namespace', namespace])
    assert result.returncode != 0
    assert "the following arguments are required: --name" in result.stderr

def test_uuid_v5_missing_namespace():
    name = "testname"
    result = run_util_command(['uuid', 'v5', '--name', name])
    assert result.returncode != 0
    assert "the following arguments are required: --namespace" in result.stderr

def test_uuid_v5_invalid_namespace():
    name = "testname"
    invalid_namespace = "not-a-uuid"
    result = run_util_command(['uuid', 'v5', '--name', name, '--namespace', invalid_namespace])
    assert result.returncode != 0
    assert f"Error: Invalid namespace UUID '{invalid_namespace}'" in result.stdout # stdout because we print the error in the command itself
