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
# CSV TO JSON TESTS
# ============================================================================


def test_convert_tabular_csv_to_json():
    """Test converting CSV to JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = os.path.join(tmpdir, "test.csv")
        with open(csv_file, "w") as f:
            f.write("name,age,city\n")
            f.write("Alice,30,New York\n")
            f.write("Bob,25,Boston\n")

        result = run_util_command(["convert", "tabular", csv_file, "json"])
        assert result.returncode == 0

        data = json.loads(result.stdout)
        assert len(data) == 2
        assert data[0]["name"] == "Alice"
        assert data[0]["age"] == "30"
        assert data[0]["city"] == "New York"


def test_convert_tabular_csv_to_json_empty():
    """Test converting empty CSV to JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = os.path.join(tmpdir, "test.csv")
        with open(csv_file, "w") as f:
            f.write("name,age,city\n")

        result = run_util_command(["convert", "tabular", csv_file, "json"])
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data == []


# ============================================================================
# JSON TO CSV TESTS
# ============================================================================


def test_convert_tabular_json_to_csv():
    """Test converting JSON to CSV."""
    with tempfile.TemporaryDirectory() as tmpdir:
        json_file = os.path.join(tmpdir, "test.json")
        data = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "Boston"},
        ]
        with open(json_file, "w") as f:
            json.dump(data, f)

        result = run_util_command(["convert", "tabular", json_file, "csv"])
        assert result.returncode == 0

        lines = result.stdout.strip().split("\n")
        assert len(lines) == 3  # Header + 2 data rows
        assert "name" in lines[0]
        assert "Alice" in lines[1]
        assert "Bob" in lines[2]


def test_convert_tabular_json_to_csv_single_object():
    """Test converting single JSON object to CSV."""
    with tempfile.TemporaryDirectory() as tmpdir:
        json_file = os.path.join(tmpdir, "test.json")
        data = {"name": "Alice", "age": 30}
        with open(json_file, "w") as f:
            json.dump(data, f)

        result = run_util_command(["convert", "tabular", json_file, "csv"])
        assert result.returncode == 0

        lines = result.stdout.strip().split("\n")
        assert len(lines) == 2  # Header + 1 data row


def test_convert_tabular_json_to_csv_missing_fields():
    """Test converting JSON with missing fields to CSV."""
    with tempfile.TemporaryDirectory() as tmpdir:
        json_file = os.path.join(tmpdir, "test.json")
        data = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25},  # Missing city
        ]
        with open(json_file, "w") as f:
            json.dump(data, f)

        result = run_util_command(["convert", "tabular", json_file, "csv"])
        assert result.returncode == 0

        lines = result.stdout.strip().split("\n")
        assert len(lines) == 3


# ============================================================================
# CSV TO MARKDOWN TESTS
# ============================================================================


def test_convert_tabular_csv_to_markdown():
    """Test converting CSV to Markdown table."""
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = os.path.join(tmpdir, "test.csv")
        with open(csv_file, "w") as f:
            f.write("name,age,city\n")
            f.write("Alice,30,New York\n")
            f.write("Bob,25,Boston\n")

        result = run_util_command(["convert", "tabular", csv_file, "markdown"])
        assert result.returncode == 0

        output = result.stdout.strip()
        lines = output.split("\n")
        assert len(lines) == 4  # Header + separator + 2 data rows
        assert "|" in lines[0]
        assert "---" in lines[1]
        assert "Alice" in lines[2]
        assert "Bob" in lines[3]


def test_convert_tabular_csv_to_markdown_alias():
    """Test using 'table' alias for markdown."""
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = os.path.join(tmpdir, "test.csv")
        with open(csv_file, "w") as f:
            f.write("name,age\n")
            f.write("Alice,30\n")

        result = run_util_command(["convert", "table", csv_file, "table"])
        assert result.returncode == 0
        assert "|" in result.stdout


# ============================================================================
# JSON TO MARKDOWN TESTS
# ============================================================================


def test_convert_tabular_json_to_markdown():
    """Test converting JSON to Markdown table."""
    with tempfile.TemporaryDirectory() as tmpdir:
        json_file = os.path.join(tmpdir, "test.json")
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
        ]
        with open(json_file, "w") as f:
            json.dump(data, f)

        result = run_util_command(["convert", "tabular", json_file, "md"])
        assert result.returncode == 0

        output = result.stdout.strip()
        lines = output.split("\n")
        assert len(lines) == 4  # Header + separator + 2 data rows
        assert "|" in lines[0]
        assert "---" in lines[1]


# ============================================================================
# ROUNDTRIP TESTS
# ============================================================================


def test_convert_tabular_roundtrip_csv_json_csv():
    """Test roundtrip CSV -> JSON -> CSV."""
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_file = os.path.join(tmpdir, "test.csv")
        json_file = os.path.join(tmpdir, "test.json")

        # Original CSV
        with open(csv_file, "w") as f:
            f.write("name,age\n")
            f.write("Alice,30\n")
            f.write("Bob,25\n")

        # Convert to JSON
        result1 = run_util_command(["convert", "tabular", csv_file, "json"])
        assert result1.returncode == 0

        with open(json_file, "w") as f:
            f.write(result1.stdout)

        # Convert back to CSV
        result2 = run_util_command(["convert", "tabular", json_file, "csv"])
        assert result2.returncode == 0

        lines = result2.stdout.strip().split("\n")
        assert len(lines) == 3  # Header + 2 data rows
        assert "Alice" in result2.stdout
        assert "Bob" in result2.stdout


# ============================================================================
# ERROR TESTS
# ============================================================================


def test_convert_tabular_file_not_found():
    """Test error when input file doesn't exist."""
    result = run_util_command(["convert", "tabular", "/tmp/nonexistent.csv", "json"])
    assert result.returncode != 0
    assert "not found" in result.stderr.lower() or "error" in result.stderr.lower()


def test_convert_tabular_invalid_json():
    """Test error with invalid JSON."""
    with tempfile.TemporaryDirectory() as tmpdir:
        json_file = os.path.join(tmpdir, "test.json")
        with open(json_file, "w") as f:
            f.write("not valid json")

        result = run_util_command(["convert", "tabular", json_file, "csv"])
        assert result.returncode != 0


def test_convert_tabular_unsupported_format():
    """Test error with unsupported file format."""
    with tempfile.TemporaryDirectory() as tmpdir:
        txt_file = os.path.join(tmpdir, "test.txt")
        with open(txt_file, "w") as f:
            f.write("test")

        result = run_util_command(["convert", "tabular", txt_file, "json"])
        assert result.returncode != 0
        assert (
            "unsupported" in result.stderr.lower() or "error" in result.stderr.lower()
        )


# ============================================================================
# HELP TESTS
# ============================================================================


def test_convert_tabular_help():
    """Test tabular conversion help."""
    result = run_util_command(["convert", "tabular", "--help"])
    assert result.returncode == 0
    assert "tabular" in result.stdout.lower() or "table" in result.stdout.lower()


def test_convert_tabular_alias_help():
    """Test table alias help."""
    result = run_util_command(["convert", "table", "--help"])
    assert result.returncode == 0
