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
- **case** - Convert text case formats (camelCase, snake_case, kebab-case, etc.)
- **completion** - Generate shell autocompletion scripts
- **convert** - Convert between formats (colors, numbers, files, configs, documents, text, tabular)
- **encode** - Encode/decode text (URL, HTML, base64, hex, morse, QR codes, binary, ROT13, and more)
- **hash** - Cryptographic hash digests (MD5, SHA1, SHA224, SHA256, SHA384, SHA512)
- **lorem** - Generate Lorem Ipsum text
- **random** - Generate random data (integers, floats, strings, etc.)
- **token** - Generate secure tokens and passwords
- **uuid** - Generate UUIDs (v1, v3, v4, v5)
- **validate** - Validate syntax, formats, and checksums (JSON, YAML, XML, HTML, CSS, email, URL, IP, credit cards, UUIDs, base64, dates, passwords, regex, cron, checksums)

## Quick Examples

```bash
# Base64 encoding/decoding
util base64 encode "Hello, World!"
util base64 decode "SGVsbG8sIFdvcmxkIQ=="

# Convert text case
util case camel "hello world"           # helloWorld
util case pascal "hello world"          # HelloWorld
util case snake "HelloWorld"            # hello_world
util case constant "hello world"        # HELLO_WORLD
util case kebab "helloWorld"            # hello-world
util case header "hello world"          # Hello-World
util case title "hello world"           # Hello World
util case sentence "HELLO WORLD"        # Hello world

# Fun text transformations
util case leet "hello world"            # h3110 w0r1d
util case upside-down "hello"           # oʃʃǝɥ
util case reverse "hello"               # olleh
util case zalgo "hello"                 # h̷e̴l̶l̴o̷ (glitch text)
util case mock "hello world"            # hElLo WoRlD

# Convert formats
util convert color "#ff0000" rgb        # rgb(255, 0, 0)
util convert base dec 255 bin           # 11111111
util convert data 1048576 auto          # 1.00 MB
util convert config package.json yaml   # Output YAML
util convert file image.png image.jpg   # Convert images
util convert tabular data.csv json      # CSV to JSON

# Encode/decode text
util encode url encode "hello world"    # hello%20world
util encode base64 encode "Hello!"      # SGVsbG8h
util encode hex encode "test"           # 74657374
util encode morse encode "SOS"          # ... --- ...
util encode rot13 "Hello"               # Uryyb
util encode qr "https://example.com"    # QR code in terminal!

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

# Validate data
util validate syntax json '{"valid": true}'    # Direct content
util validate syntax yaml config.yaml          # File (auto-detected)
util validate email "user@example.com"
util validate url "https://github.com/user/repo"
util validate ip "192.168.1.1"
util validate card "4532-0151-1283-0366"
util validate uuid "550e8400-e29b-41d4-a716-446655440000"
util validate base64 "SGVsbG8gV29ybGQ="
util validate date "2024-01-15T10:30:00Z"
util validate password "MyP@ssw0rd123!"
util validate regex "^[a-z]+$"
util validate cron "0 */2 * * *"
util validate checksum file.txt abc123def456 --algorithm sha256
```

## Usage Tips

```bash
# Get help for any command
util --help
util case --help
util random --help
util token password --help

# Combine with other tools
PASSWORD=$(util token password --length 20 --special)
echo "Password: $PASSWORD"

# Generate API keys
export API_KEY=$(util token hex --bytes 32)

# Convert variable names
VAR_NAME="user profile data"
echo "camelCase: $(util case camel "$VAR_NAME")"      # userProfileData
echo "snake_case: $(util case snake "$VAR_NAME")"     # user_profile_data
echo "CONSTANT: $(util case constant "$VAR_NAME")"    # USER_PROFILE_DATA

# Convert config formats
util convert config package.json yaml > package.yaml
util convert config docker-compose.yml toml > config.toml

# Convert documents
util convert doc README.md README.html
util convert doc README.md README.pdf
util convert doc notes.md notes.docx

# Batch convert images
for img in *.png; do
  util convert file "$img" "${img%.png}.jpg"
done

# Text encoding/escaping in scripts
URL="https://example.com/search?q=$(util convert text url-encode "hello world")"
SQL_SAFE=$(util convert text escape "User's input" --target sql)

# CSV/JSON data processing
util convert tabular users.csv json | jq '.[] | select(.age > 30)'
util convert tabular api_data.json markdown > report.md

# Encode data in scripts
ENCODED_DATA=$(util encode base64 encode "sensitive data")
URL_PARAM=$(util encode url encode "user input")
echo "Morse: $(util encode morse encode "HELP")"
util encode qr "https://yourapp.com/share/$(util token hex 16)"  # QR code with unique URL

# Decode operations
util encode base64 decode "$ENCODED_DATA"
util encode url decode "$URL_PARAM"

# Fun text transformations
echo "Make it 1337: $(util case leet 'hello hacker')"
echo "Upside down: $(util case upside-down 'wow')"
echo "Spooky text: $(util case zalgo 'boo')"
echo "$(util case mock 'oh really')"  # Mock someone

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
│       ├── case.py
│       ├── case_data.py     # Text transformation mappings
│       ├── completion.py
│       ├── convert/         # Modular conversion commands
│       │   ├── base.py      # Number base conversions
│       │   ├── color.py     # Color format conversions
│       │   ├── config.py    # Config file conversions (JSON/YAML/TOML/XML)
│       │   ├── data.py      # Data size conversions
│       │   ├── document.py  # Document conversions (Pandoc)
│       │   ├── file.py      # Image/video/audio conversions
│       │   ├── tabular.py   # Tabular data conversions (CSV/JSON/Markdown)
│       │   ├── text.py      # Text encoding/escaping conversions
│       │   └── time.py      # Time format conversions
│       ├── encode.py
│       ├── hash.py
│       ├── lorem.py
│       ├── random.py
│       ├── token.py
│       ├── uuid.py
│       └── validate.py
└── tests/                   # Test suite (402 tests)
```

## Requirements

### Core Dependencies (auto-installed)

- Python 3.7+
- argcomplete - Shell autocompletion
- lorem-text - Lorem Ipsum generation
- Pillow - Image conversions
- PyYAML, tomli, tomli-w, xmltodict - Config file conversions
- qrcode[pil] - QR code generation

### Optional Dependencies (for advanced features)

- **FFmpeg** - Video/audio file conversions
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`
- **Pandoc** - Document conversions (40+ formats)
  - macOS: `brew install pandoc`
  - Linux: `sudo apt install pandoc`
- **LaTeX** - PDF generation (via Pandoc)
  - macOS: `brew install --cask basictex`
  - Linux: `sudo apt install texlive`

## License

MIT License
