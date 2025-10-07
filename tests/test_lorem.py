import subprocess
import pytest

# Helper function to run the util command
def run_util_command(command_args):
    full_command = ['python', '-m', 'util.main'] + command_args
    result = subprocess.run(full_command, capture_output=True, text=True, check=False)
    return result

def test_lorem_default_paragraphs():
    result = run_util_command(['lorem', 'paragraphs'])
    assert result.returncode == 0
    # Check if it contains at least one paragraph (lorem_text generates multiple sentences per paragraph)
    assert len([p for p in result.stdout.strip().split('\n\n') if p]) >= 1
    assert len(result.stdout.strip().split(' ')) > 10 # Should be more than 10 words

def test_lorem_specific_paragraphs():
    result = run_util_command(['lorem', 'paragraphs', '--count', '3'])
    assert result.returncode == 0
    assert len([p for p in result.stdout.strip().split('\n\n') if p]) >= 3

def test_lorem_specific_paragraphs_alias():
    result = run_util_command(['lorem', 'p', '--count', '3'])
    assert result.returncode == 0
    assert len([p for p in result.stdout.strip().split('\n\n') if p]) >= 3

def test_lorem_specific_sentences():
    result = run_util_command(['lorem', 'sentences', '--count', '5'])
    assert result.returncode == 0
    # Since we are generating sentences one by one, we expect 5 sentences, each ending with a period.
    # The lorem_text library's sentence() method might not always end with a period, so we check word count.
    assert len(result.stdout.strip().split(' ')) > 5 # Should be more than 5 words

def test_lorem_specific_sentences_alias():
    result = run_util_command(['lorem', 's', '--count', '5'])
    assert result.returncode == 0
    assert len(result.stdout.strip().split(' ')) > 5 # Should be more than 5 words

def test_lorem_specific_words():
    result = run_util_command(['lorem', 'words', '--count', '10'])
    assert result.returncode == 0
    assert len([word for word in result.stdout.strip().split(' ') if word]) >= 10

def test_lorem_specific_words_alias():
    result = run_util_command(['lorem', 'w', '--count', '10'])
    assert result.returncode == 0
    assert len([word for word in result.stdout.strip().split(' ') if word]) >= 10

def test_lorem_invalid_count_type():
    result = run_util_command(['lorem', 'paragraphs', '--count', 'abc'])
    assert result.returncode != 0
    assert "invalid int value: 'abc'" in result.stderr

def test_lorem_negative_count():
    # lorem_text library handles negative counts by returning empty string or raising error
    # Let's check if it returns empty or handles gracefully
    result = run_util_command(['lorem', 'paragraphs', '--count', '-1'])
    assert result.returncode == 0 # The library doesn't raise an error, just returns empty
    assert result.stdout.strip() == ""