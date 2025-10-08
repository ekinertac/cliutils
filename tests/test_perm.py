import subprocess


def run_util_command(args):
    """Helper function to run util command as a subprocess."""
    result = subprocess.run(
        ["python", "-m", "util.main"] + args,
        capture_output=True,
        text=True,
    )
    return result


# ============================================================================
# CONVERT TESTS
# ============================================================================


def test_perm_convert_octal_to_symbolic():
    """Test converting octal to symbolic (auto-detect)."""
    result = run_util_command(["perm", "convert", "755"])
    assert result.returncode == 0
    assert result.stdout.strip() == "rwxr-xr-x"


def test_perm_convert_octal_to_symbolic_644():
    """Test converting 644 to symbolic (auto-detect)."""
    result = run_util_command(["perm", "convert", "644"])
    assert result.returncode == 0
    assert result.stdout.strip() == "rw-r--r--"


def test_perm_convert_octal_to_symbolic_777():
    """Test converting 777 to symbolic (auto-detect)."""
    result = run_util_command(["perm", "convert", "777"])
    assert result.returncode == 0
    assert result.stdout.strip() == "rwxrwxrwx"


def test_perm_convert_octal_to_symbolic_000():
    """Test converting 000 to symbolic (auto-detect)."""
    result = run_util_command(["perm", "convert", "000"])
    assert result.returncode == 0
    assert result.stdout.strip() == "---------"


def test_perm_convert_symbolic_to_octal():
    """Test converting symbolic to octal (auto-detect)."""
    result = run_util_command(["perm", "convert", "rwxr-xr-x"])
    assert result.returncode == 0
    assert result.stdout.strip() == "755"


def test_perm_convert_symbolic_to_octal_644():
    """Test converting rw-r--r-- to octal (auto-detect)."""
    result = run_util_command(["perm", "convert", "rw-r--r--"])
    assert result.returncode == 0
    assert result.stdout.strip() == "644"


def test_perm_convert_symbolic_to_octal_600():
    """Test converting rw------- to octal (auto-detect)."""
    result = run_util_command(["perm", "convert", "rw-------"])
    assert result.returncode == 0
    assert result.stdout.strip() == "600"


def test_perm_convert_octal_to_binary():
    """Test converting octal to binary (explicit)."""
    result = run_util_command(["perm", "convert", "755", "--to", "binary"])
    assert result.returncode == 0
    output = result.stdout.strip()
    assert "Owner: 111" in output
    assert "Group: 101" in output
    assert "Other: 101" in output


def test_perm_convert_octal_to_binary_644():
    """Test converting 644 to binary (explicit)."""
    result = run_util_command(["perm", "convert", "644", "--to", "binary"])
    assert result.returncode == 0
    output = result.stdout.strip()
    assert "Owner: 110" in output
    assert "Group: 100" in output
    assert "Other: 100" in output


# ============================================================================
# SPECIAL PERMISSIONS TESTS
# ============================================================================


def test_perm_convert_setuid():
    """Test converting setuid permission (auto-detect)."""
    result = run_util_command(["perm", "convert", "4755"])
    assert result.returncode == 0
    assert result.stdout.strip() == "rwsr-xr-x"


def test_perm_convert_setgid():
    """Test converting setgid permission (auto-detect)."""
    result = run_util_command(["perm", "convert", "2755"])
    assert result.returncode == 0
    assert result.stdout.strip() == "rwxr-sr-x"


def test_perm_convert_sticky():
    """Test converting sticky bit permission (auto-detect)."""
    result = run_util_command(["perm", "convert", "1777"])
    assert result.returncode == 0
    assert result.stdout.strip() == "rwxrwxrwt"


def test_perm_convert_setuid_symbolic_to_octal():
    """Test converting symbolic setuid to octal (auto-detect)."""
    result = run_util_command(["perm", "convert", "rwsr-xr-x"])
    assert result.returncode == 0
    assert result.stdout.strip() == "4755"


def test_perm_convert_setgid_symbolic_to_octal():
    """Test converting symbolic setgid to octal (auto-detect)."""
    result = run_util_command(["perm", "convert", "rwxr-sr-x"])
    assert result.returncode == 0
    assert result.stdout.strip() == "2755"


def test_perm_convert_sticky_symbolic_to_octal():
    """Test converting symbolic sticky to octal (auto-detect)."""
    result = run_util_command(["perm", "convert", "rwxrwxrwt"])
    assert result.returncode == 0
    assert result.stdout.strip() == "1777"


def test_perm_convert_setuid_no_execute():
    """Test setuid without execute (capital S) (auto-detect)."""
    result = run_util_command(["perm", "convert", "4644"])
    assert result.returncode == 0
    assert result.stdout.strip() == "rwSr--r--"


def test_perm_convert_sticky_no_execute():
    """Test sticky without execute (capital T) (auto-detect)."""
    result = run_util_command(["perm", "convert", "1666"])
    assert result.returncode == 0
    assert result.stdout.strip() == "rw-rw-rwT"


# ============================================================================
# EXPLAIN TESTS
# ============================================================================


def test_perm_explain_755():
    """Test explaining 755 permissions."""
    result = run_util_command(["perm", "explain", "755"])
    assert result.returncode == 0
    output = result.stdout
    assert "755" in output
    assert "rwxr-xr-x" in output
    assert "Owner" in output
    assert "Group" in output
    assert "Other" in output
    assert "chmod 755" in output


def test_perm_explain_644():
    """Test explaining 644 permissions."""
    result = run_util_command(["perm", "explain", "644"])
    assert result.returncode == 0
    output = result.stdout
    assert "644" in output
    assert "rw-r--r--" in output
    assert "read, write" in output


def test_perm_explain_777():
    """Test explaining 777 permissions."""
    result = run_util_command(["perm", "explain", "777"])
    assert result.returncode == 0
    output = result.stdout
    assert "777" in output
    assert "rwxrwxrwx" in output


# ============================================================================
# CALCULATION TESTS
# ============================================================================


def test_perm_calc_add():
    """Test adding permissions (add execute)."""
    result = run_util_command(["perm", "calc", "add", "644", "111"])
    assert result.returncode == 0
    output = result.stdout.strip()
    assert "755" in output
    assert "rwxr-xr-x" in output


def test_perm_calc_add_write():
    """Test adding write permissions."""
    result = run_util_command(["perm", "calc", "add", "444", "222"])
    assert result.returncode == 0
    output = result.stdout.strip()
    assert "666" in output


def test_perm_calc_remove():
    """Test removing permissions (remove execute)."""
    result = run_util_command(["perm", "calc", "remove", "755", "111"])
    assert result.returncode == 0
    output = result.stdout.strip()
    assert "644" in output
    assert "rw-r--r--" in output


def test_perm_calc_remove_write():
    """Test removing write permissions."""
    result = run_util_command(["perm", "calc", "remove", "666", "222"])
    assert result.returncode == 0
    output = result.stdout.strip()
    assert "444" in output


def test_perm_calc_mask():
    """Test masking permissions."""
    result = run_util_command(["perm", "calc", "mask", "777", "755"])
    assert result.returncode == 0
    output = result.stdout.strip()
    assert "755" in output


def test_perm_calc_mask_readonly():
    """Test masking to read-only."""
    result = run_util_command(["perm", "calc", "mask", "777", "444"])
    assert result.returncode == 0
    output = result.stdout.strip()
    assert "444" in output


# ============================================================================
# COMMON PERMISSIONS TESTS
# ============================================================================


def test_perm_common():
    """Test listing common permissions."""
    result = run_util_command(["perm", "common"])
    assert result.returncode == 0
    output = result.stdout
    assert "644" in output
    assert "755" in output
    assert "777" in output
    assert "rw-r--r--" in output
    assert "rwxr-xr-x" in output
    assert "Files:" in output
    assert "Executables" in output


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================


def test_perm_convert_invalid_octal():
    """Test error handling for invalid octal."""
    result = run_util_command(["perm", "convert", "888"])
    assert result.returncode != 0
    assert "error" in result.stderr.lower()


def test_perm_convert_invalid_symbolic():
    """Test error handling for invalid symbolic."""
    result = run_util_command(["perm", "convert", "rwxrwxrw"])
    assert result.returncode != 0
    assert "error" in result.stderr.lower()


def test_perm_convert_invalid_symbolic_chars():
    """Test error handling for invalid characters in symbolic."""
    result = run_util_command(["perm", "convert", "rwxrwxabc"])
    assert result.returncode != 0
    assert "error" in result.stderr.lower()


def test_perm_explain_invalid():
    """Test error handling for invalid permission in explain."""
    result = run_util_command(["perm", "explain", "999"])
    assert result.returncode != 0
    assert "error" in result.stderr.lower()


# ============================================================================
# HELP TESTS
# ============================================================================


def test_perm_help():
    """Test perm help."""
    result = run_util_command(["perm", "--help"])
    assert result.returncode == 0
    assert "perm" in result.stdout.lower()
    assert "convert" in result.stdout.lower()
    assert "explain" in result.stdout.lower()


def test_perm_convert_help():
    """Test perm convert help."""
    result = run_util_command(["perm", "convert", "--help"])
    assert result.returncode == 0
    assert "convert" in result.stdout.lower()
    assert "symbolic" in result.stdout.lower()
    assert "octal" in result.stdout.lower()


def test_perm_no_arguments():
    """Test error when no arguments provided."""
    result = run_util_command(["perm"])
    assert result.returncode != 0
    assert "required" in result.stderr.lower() or "error" in result.stderr.lower()


# ============================================================================
# ROUNDTRIP TESTS
# ============================================================================


def test_perm_roundtrip_755():
    """Test roundtrip conversion for 755 (auto-detect)."""
    # Octal -> Symbolic
    result1 = run_util_command(["perm", "convert", "755"])
    symbolic = result1.stdout.strip()
    # Symbolic -> Octal
    result2 = run_util_command(["perm", "convert", symbolic])
    assert result2.stdout.strip() == "755"


def test_perm_roundtrip_644():
    """Test roundtrip conversion for 644 (auto-detect)."""
    result1 = run_util_command(["perm", "convert", "644"])
    symbolic = result1.stdout.strip()
    result2 = run_util_command(["perm", "convert", symbolic])
    assert result2.stdout.strip() == "644"


def test_perm_roundtrip_special():
    """Test roundtrip conversion for special permissions (auto-detect)."""
    result1 = run_util_command(["perm", "convert", "4755"])
    symbolic = result1.stdout.strip()
    result2 = run_util_command(["perm", "convert", symbolic])
    assert result2.stdout.strip() == "4755"
