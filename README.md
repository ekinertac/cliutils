# cliutils

A modular command-line utility collection providing common tools for developers. Built with Python, featuring argparse for robust CLI parsing and argcomplete for shell autocompletion.

## Installation

```bash
# Clone and install
git clone <repository-url>
cd cliutils
pip install -e .

# Enable autocompletion (optional)
activate-global-python-argcomplete
```

## Commands

- **base64** - Encode/decode base64
- **hash** - Cryptographic hash digests (MD5, SHA1, SHA224, SHA256, SHA384, SHA512)
- **lorem** - Generate Lorem Ipsum text
- **random** - Generate random data (integers, floats, strings, etc.)
- **token** - Generate secure tokens and passwords
- **uuid** - Generate UUIDs (v1, v3, v4, v5)
- **completion** - Generate shell autocompletion scripts

## Quick Examples

```bash
# Base64 encoding/decoding
util base64 encode "Hello, World!" # Output: SGVsbG8sIFdvcmxkIQ==
util base64 decode "SGVsbG8sIFdvcmxkIQ=="

# Generate hashes
util hash sha256 "password123"
util hash md5 "test"

# Generate Lorem Ipsum
util lorem paragraphs 3
util lorem sentences 10
util lorem words 50

util lorem p 3
util lorem s 10
util lorem w 50

# Generate random data
util random int --min 1 --max 100
util random float --min 0.0 --max 1.0
util random string --length 20
util random string --length 15 --lowercase --digits
util random choice apple banana orange
util random shuffle 1 2 3 4 5

# Generate secure tokens
util token hex --bytes 32
util token urlsafe
util token password --length 24 --special

# Generate UUIDs
util uuid
util uuid v1
util uuid v5 --name "user@example.com" --namespace "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
```

## Usage Tips

```bash
# Get help for any command
util --help
util random --help
util token password --help

# Combine with other tools
PASSWORD=$(util token password --length 20 --special)
echo "Password: $PASSWORD"

# Generate API keys
export API_KEY=$(util token hex --bytes 32)

# Create test data
for i in {1..10}; do
  echo "$(util uuid),$(util lorem words --count 2),$(util random int --min 18 --max 80)"
done
```

## Testing

```bash
pytest
pytest -v  # verbose output
```

## Adding New Commands

Create a file in `util/commands/` with a `setup_parser()` function:

```python
def setup_parser(subparsers):
    parser = subparsers.add_parser('mycommand', help='Description')
    parser.add_argument('--option', help='Option help')
    parser.set_defaults(func=my_function)
```

The command will be automatically discovered!

## Project Structure

```
cliutils/
├── util/
│   ├── main.py              # CLI entry point
│   └── commands/            # Command modules
│       ├── base64.py
│       ├── hash.py
│       ├── lorem.py
│       ├── random.py
│       ├── token.py
│       └── uuid.py
└── tests/                   # Test suite
```

## Requirements

- Python 3.7+
- argcomplete
- lorem-text

## License

MIT License
