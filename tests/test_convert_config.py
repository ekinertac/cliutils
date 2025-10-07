import json
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
# JSON CONVERSION TESTS
# ============================================================================


def test_convert_config_json_to_yaml():
    """Test converting JSON to YAML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.json")

        # Create test JSON
        data = {"name": "test", "version": "1.0", "items": ["a", "b", "c"]}
        with open(input_file, "w") as f:
            json.dump(data, f)

        # Convert
        result = run_util_command(["convert", "config", input_file, "yaml"])
        assert result.returncode == 0
        assert "name: test" in result.stdout
        assert "version:" in result.stdout


def test_convert_config_json_to_toml():
    """Test converting JSON to TOML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.json")

        # Create test JSON
        data = {"name": "test", "version": "1.0"}
        with open(input_file, "w") as f:
            json.dump(data, f)

        # Convert
        result = run_util_command(["convert", "config", input_file, "toml"])
        assert result.returncode == 0
        assert 'name = "test"' in result.stdout
        assert 'version = "1.0"' in result.stdout


def test_convert_config_json_to_xml():
    """Test converting JSON to XML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.json")

        # Create test JSON with root element
        data = {"root": {"name": "test", "version": "1.0"}}
        with open(input_file, "w") as f:
            json.dump(data, f)

        # Convert
        result = run_util_command(["convert", "config", input_file, "xml"])
        assert result.returncode == 0
        assert "<root>" in result.stdout
        assert "<name>" in result.stdout


# ============================================================================
# YAML CONVERSION TESTS
# ============================================================================


def test_convert_config_yaml_to_json():
    """Test converting YAML to JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.yaml")

        # Create test YAML
        yaml_content = """
name: test
version: 1.0
items:
  - a
  - b
  - c
"""
        with open(input_file, "w") as f:
            f.write(yaml_content)

        # Convert
        result = run_util_command(["convert", "config", input_file, "json"])
        assert result.returncode == 0
        assert '"name": "test"' in result.stdout
        assert '"version"' in result.stdout


def test_convert_config_yml_extension():
    """Test that .yml extension works."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.yml")

        # Create test YAML
        yaml_content = "name: test\nversion: 1.0\n"
        with open(input_file, "w") as f:
            f.write(yaml_content)

        # Convert
        result = run_util_command(["convert", "config", input_file, "json"])
        assert result.returncode == 0
        assert '"name"' in result.stdout


def test_convert_config_yaml_to_toml():
    """Test converting YAML to TOML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.yaml")

        # Create test YAML
        yaml_content = "name: test\nversion: 1.0\n"
        with open(input_file, "w") as f:
            f.write(yaml_content)

        # Convert
        result = run_util_command(["convert", "config", input_file, "toml"])
        assert result.returncode == 0
        assert 'name = "test"' in result.stdout


# ============================================================================
# TOML CONVERSION TESTS
# ============================================================================


def test_convert_config_toml_to_json():
    """Test converting TOML to JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.toml")

        # Create test TOML
        toml_content = """
name = "test"
version = "1.0"

[dependencies]
python = ">=3.7"
"""
        with open(input_file, "w") as f:
            f.write(toml_content)

        # Convert
        result = run_util_command(["convert", "config", input_file, "json"])
        assert result.returncode == 0
        assert '"name": "test"' in result.stdout
        assert '"dependencies"' in result.stdout


def test_convert_config_toml_to_yaml():
    """Test converting TOML to YAML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.toml")

        # Create test TOML
        toml_content = 'name = "test"\nversion = "1.0"\n'
        with open(input_file, "w") as f:
            f.write(toml_content)

        # Convert
        result = run_util_command(["convert", "config", input_file, "yaml"])
        assert result.returncode == 0
        assert "name: test" in result.stdout


# ============================================================================
# COMPLEX DATA TESTS
# ============================================================================


def test_convert_config_nested_structures():
    """Test converting nested data structures."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.json")

        # Create complex JSON
        data = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "credentials": {"username": "admin", "password": "secret"},
            },
            "features": {"enabled": True, "items": [1, 2, 3]},
        }
        with open(input_file, "w") as f:
            json.dump(data, f)

        # Convert to YAML
        result = run_util_command(["convert", "config", input_file, "yaml"])
        assert result.returncode == 0
        assert "database:" in result.stdout
        assert "credentials:" in result.stdout
        assert "features:" in result.stdout


def test_convert_config_arrays():
    """Test converting arrays/lists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.json")

        # Create JSON with arrays
        data = {"servers": ["web1", "web2", "web3"], "ports": [80, 443, 8080]}
        with open(input_file, "w") as f:
            json.dump(data, f)

        # Convert to YAML
        result = run_util_command(["convert", "config", input_file, "yaml"])
        assert result.returncode == 0
        assert "servers:" in result.stdout


def test_convert_config_unicode():
    """Test converting files with Unicode characters."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.json")

        # Create JSON with Unicode
        data = {"greeting": "こんにちは", "emoji": "🚀", "name": "Tést"}
        with open(input_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        # Convert to YAML
        result = run_util_command(["convert", "config", input_file, "yaml"])
        assert result.returncode == 0


# ============================================================================
# ROUNDTRIP TESTS
# ============================================================================


def test_convert_config_roundtrip_json_yaml_json():
    """Test roundtrip conversion: JSON → YAML → JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        json1_file = os.path.join(tmpdir, "test1.json")
        yaml_file = os.path.join(tmpdir, "test.yaml")
        json2_file = os.path.join(tmpdir, "test2.json")

        # Create original JSON
        data = {"name": "test", "version": "1.0", "count": 42}
        with open(json1_file, "w") as f:
            json.dump(data, f)

        # Convert to YAML
        result1 = run_util_command(["convert", "config", json1_file, "yaml"])
        assert result1.returncode == 0
        with open(yaml_file, "w") as f:
            f.write(result1.stdout)

        # Convert back to JSON
        result2 = run_util_command(["convert", "config", yaml_file, "json"])
        assert result2.returncode == 0

        # Parse and compare
        result_data = json.loads(result2.stdout)
        assert result_data["name"] == "test"
        assert result_data["version"] == "1.0"
        assert result_data["count"] == 42


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================


def test_convert_config_file_not_found():
    """Test error when input file doesn't exist."""
    result = run_util_command(["convert", "config", "/tmp/nonexistent.json", "yaml"])
    assert result.returncode != 0
    assert "not found" in result.stderr.lower()


def test_convert_config_unsupported_extension():
    """Test error with unsupported file extension."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.txt")

        # Create a file with unsupported extension
        with open(input_file, "w") as f:
            f.write("some content")

        result = run_util_command(["convert", "config", input_file, "yaml"])
        assert result.returncode != 0
        assert (
            "detect format" in result.stderr.lower() or "error" in result.stderr.lower()
        )


def test_convert_config_invalid_json():
    """Test error with invalid JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.json")

        # Create invalid JSON
        with open(input_file, "w") as f:
            f.write("{invalid json")

        result = run_util_command(["convert", "config", input_file, "yaml"])
        assert result.returncode != 0
        assert "error" in result.stderr.lower()


def test_convert_config_invalid_yaml():
    """Test error with invalid YAML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.yaml")

        # Create invalid YAML
        with open(input_file, "w") as f:
            f.write("invalid: yaml: content: [")

        result = run_util_command(["convert", "config", input_file, "json"])
        assert result.returncode != 0
        assert "error" in result.stderr.lower()


def test_convert_config_invalid_toml():
    """Test error with invalid TOML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "test.toml")

        # Create invalid TOML
        with open(input_file, "w") as f:
            f.write("[section\ninvalid")

        result = run_util_command(["convert", "config", input_file, "json"])
        assert result.returncode != 0
        assert "error" in result.stderr.lower()


# ============================================================================
# HELP TESTS
# ============================================================================


def test_convert_config_help():
    """Test config conversion help."""
    result = run_util_command(["convert", "config", "--help"])
    assert result.returncode == 0
    assert "config" in result.stdout.lower()
    assert "json" in result.stdout.lower()
    assert "yaml" in result.stdout.lower()
    assert "toml" in result.stdout.lower()


def test_convert_config_no_arguments():
    """Test error when no arguments provided."""
    result = run_util_command(["convert", "config"])
    assert result.returncode != 0
    assert "required" in result.stderr.lower() or "error" in result.stderr.lower()
