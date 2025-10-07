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
# COLOR CONVERSION TESTS
# ============================================================================


def test_convert_color_hex_to_rgb():
    result = run_util_command(["convert", "color", "#ff0000", "rgb"])
    assert result.returncode == 0
    assert result.stdout.strip() == "rgb(255, 0, 0)"


def test_convert_color_hex_0x_to_rgb():
    result = run_util_command(["convert", "color", "0xFF0000", "rgb"])
    assert result.returncode == 0
    assert result.stdout.strip() == "rgb(255, 0, 0)"


def test_convert_color_hex_plain_to_rgb():
    result = run_util_command(["convert", "color", "ff0000", "rgb"])
    assert result.returncode == 0
    assert result.stdout.strip() == "rgb(255, 0, 0)"


def test_convert_color_rgb_to_hex():
    result = run_util_command(["convert", "color", "rgb(255, 0, 0)", "hex"])
    assert result.returncode == 0
    assert result.stdout.strip() == "#ff0000"


def test_convert_color_hex_to_hsl():
    result = run_util_command(["convert", "color", "#ff0000", "hsl"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hsl(0, 100%, 50%)"


def test_convert_color_hsl_to_hex():
    result = run_util_command(["convert", "color", "hsl(0, 100%, 50%)", "hex"])
    assert result.returncode == 0
    assert result.stdout.strip() == "#ff0000"


def test_convert_color_hex_to_int():
    result = run_util_command(["convert", "color", "#ff0000", "int"])
    assert result.returncode == 0
    assert result.stdout.strip() == "16711680"


def test_convert_color_int_to_hex():
    result = run_util_command(["convert", "color", "16711680", "hex"])
    assert result.returncode == 0
    assert result.stdout.strip() == "#ff0000"


def test_convert_color_hex_to_0x():
    result = run_util_command(["convert", "color", "#ff0000", "0x"])
    assert result.returncode == 0
    assert result.stdout.strip() == "0xFF0000"


def test_convert_color_rgb_to_hsl():
    result = run_util_command(["convert", "color", "rgb(255, 0, 0)", "hsl"])
    assert result.returncode == 0
    assert result.stdout.strip() == "hsl(0, 100%, 50%)"


def test_convert_color_hsl_to_rgb():
    result = run_util_command(["convert", "color", "hsl(120, 100%, 50%)", "rgb"])
    assert result.returncode == 0
    assert result.stdout.strip() == "rgb(0, 255, 0)"


def test_convert_color_short_hex():
    result = run_util_command(["convert", "color", "#f00", "rgb"])
    assert result.returncode == 0
    assert result.stdout.strip() == "rgb(255, 0, 0)"


def test_convert_color_blue():
    result = run_util_command(["convert", "color", "#0000ff", "rgb"])
    assert result.returncode == 0
    assert result.stdout.strip() == "rgb(0, 0, 255)"


def test_convert_color_white():
    result = run_util_command(["convert", "color", "#ffffff", "rgb"])
    assert result.returncode == 0
    assert result.stdout.strip() == "rgb(255, 255, 255)"


def test_convert_color_black():
    result = run_util_command(["convert", "color", "#000000", "rgb"])
    assert result.returncode == 0
    assert result.stdout.strip() == "rgb(0, 0, 0)"


# ============================================================================
# BASE CONVERSION TESTS
# ============================================================================


def test_convert_base_dec_to_bin():
    result = run_util_command(["convert", "base", "dec", "255", "bin"])
    assert result.returncode == 0
    assert result.stdout.strip() == "11111111"


def test_convert_base_dec_to_hex():
    result = run_util_command(["convert", "base", "dec", "255", "hex"])
    assert result.returncode == 0
    assert result.stdout.strip() == "ff"


def test_convert_base_dec_to_oct():
    result = run_util_command(["convert", "base", "dec", "255", "oct"])
    assert result.returncode == 0
    assert result.stdout.strip() == "377"


def test_convert_base_hex_to_dec():
    result = run_util_command(["convert", "base", "hex", "ff", "dec"])
    assert result.returncode == 0
    assert result.stdout.strip() == "255"


def test_convert_base_hex_0x_to_dec():
    result = run_util_command(["convert", "base", "hex", "0xFF", "dec"])
    assert result.returncode == 0
    assert result.stdout.strip() == "255"


def test_convert_base_bin_to_dec():
    result = run_util_command(["convert", "base", "bin", "11111111", "dec"])
    assert result.returncode == 0
    assert result.stdout.strip() == "255"


def test_convert_base_oct_to_dec():
    result = run_util_command(["convert", "base", "oct", "377", "dec"])
    assert result.returncode == 0
    assert result.stdout.strip() == "255"


def test_convert_base_dec_to_0x():
    result = run_util_command(["convert", "base", "dec", "255", "0x"])
    assert result.returncode == 0
    assert result.stdout.strip() == "0xff"


def test_convert_base_dec_to_0b():
    result = run_util_command(["convert", "base", "dec", "255", "0b"])
    assert result.returncode == 0
    assert result.stdout.strip() == "0b11111111"


def test_convert_base_hex_to_bin():
    result = run_util_command(["convert", "base", "hex", "ff", "bin"])
    assert result.returncode == 0
    assert result.stdout.strip() == "11111111"


def test_convert_base_bin_to_hex():
    result = run_util_command(["convert", "base", "bin", "11111111", "hex"])
    assert result.returncode == 0
    assert result.stdout.strip() == "ff"


def test_convert_base_zero():
    result = run_util_command(["convert", "base", "dec", "0", "bin"])
    assert result.returncode == 0
    assert result.stdout.strip() == "0"


def test_convert_base_large_number():
    result = run_util_command(["convert", "base", "dec", "1024", "hex"])
    assert result.returncode == 0
    assert result.stdout.strip() == "400"


# ============================================================================
# DATA SIZE CONVERSION TESTS
# ============================================================================


def test_convert_data_bytes_to_kb():
    result = run_util_command(["convert", "data", "1024", "kb"])
    assert result.returncode == 0
    assert result.stdout.strip() == "1.00 KB"


def test_convert_data_bytes_to_mb():
    result = run_util_command(["convert", "data", "1048576", "mb"])
    assert result.returncode == 0
    assert result.stdout.strip() == "1.00 MB"


def test_convert_data_kb_to_mb():
    result = run_util_command(["convert", "data", "1024KB", "mb"])
    assert result.returncode == 0
    assert result.stdout.strip() == "1.00 MB"


def test_convert_data_mb_to_gb():
    result = run_util_command(["convert", "data", "1024MB", "gb"])
    assert result.returncode == 0
    assert result.stdout.strip() == "1.00 GB"


def test_convert_data_gb_to_mb():
    result = run_util_command(["convert", "data", "1GB", "mb"])
    assert result.returncode == 0
    assert result.stdout.strip() == "1024.00 MB"


def test_convert_data_auto_bytes():
    result = run_util_command(["convert", "data", "512", "auto"])
    assert result.returncode == 0
    assert result.stdout.strip() == "512 B"


def test_convert_data_auto_kb():
    result = run_util_command(["convert", "data", "2048", "auto"])
    assert result.returncode == 0
    assert result.stdout.strip() == "2.00 KB"


def test_convert_data_auto_mb():
    result = run_util_command(["convert", "data", "5242880", "auto"])
    assert result.returncode == 0
    assert result.stdout.strip() == "5.00 MB"


def test_convert_data_decimal_input():
    result = run_util_command(["convert", "data", "1.5MB", "kb"])
    assert result.returncode == 0
    assert result.stdout.strip() == "1536.00 KB"


def test_convert_data_to_bytes():
    result = run_util_command(["convert", "data", "1KB", "bytes"])
    assert result.returncode == 0
    assert result.stdout.strip() == "1024 B"


# ============================================================================
# TIME CONVERSION TESTS
# ============================================================================


def test_convert_time_unix_to_iso():
    result = run_util_command(["convert", "time", "unix", "1699564800", "iso"])
    assert result.returncode == 0
    # Should contain a valid ISO timestamp
    assert (
        "2023-11-10" in result.stdout or "2023-11-09" in result.stdout
    )  # Timezone difference


def test_convert_time_unix_to_date():
    result = run_util_command(["convert", "time", "unix", "1699564800", "date"])
    assert result.returncode == 0
    # Should contain a date
    assert "2023-11-" in result.stdout


def test_convert_time_unix_to_datetime():
    result = run_util_command(["convert", "time", "unix", "1699564800", "datetime"])
    assert result.returncode == 0
    # Should contain date and time
    assert "2023-11-" in result.stdout
    assert ":" in result.stdout


def test_convert_time_iso_to_unix():
    result = run_util_command(["convert", "time", "iso", "2023-11-10T00:00:00", "unix"])
    assert result.returncode == 0
    # Should be a valid unix timestamp
    timestamp = int(result.stdout.strip())
    assert timestamp > 0


def test_convert_time_zero():
    result = run_util_command(["convert", "time", "unix", "0", "iso"])
    assert result.returncode == 0
    # Should be around 1970-01-01
    assert "1970" in result.stdout or "1969" in result.stdout  # Timezone difference


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================


def test_convert_no_arguments():
    result = run_util_command(["convert"])
    assert result.returncode != 0


def test_convert_color_invalid_format():
    result = run_util_command(["convert", "color", "invalid", "rgb"])
    assert result.returncode != 0
    assert "error" in result.stderr.lower()


def test_convert_base_invalid_value():
    result = run_util_command(["convert", "base", "hex", "xyz", "dec"])
    assert result.returncode != 0
    assert "error" in result.stderr.lower()


def test_convert_help():
    result = run_util_command(["convert", "--help"])
    assert result.returncode == 0
    assert "convert" in result.stdout.lower()


def test_convert_color_help():
    result = run_util_command(["convert", "color", "--help"])
    assert result.returncode == 0
    assert "color" in result.stdout.lower()


def test_convert_base_help():
    result = run_util_command(["convert", "base", "--help"])
    assert result.returncode == 0
    assert "base" in result.stdout.lower()
