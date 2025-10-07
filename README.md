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
- **hash** - Cryptographic hash digests (MD5, SHA1, SHA224, SHA256, SHA384, SHA512)
- **lorem** - Generate Lorem Ipsum text
- **random** - Generate random data (integers, floats, strings, etc.)
- **token** - Generate secure tokens and passwords
- **uuid** - Generate UUIDs (v1, v3, v4, v5)
- **validate** - Validate syntax, formats, and checksums (JSON, YAML, XML, email, URL, IP, credit cards, checksums)

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

# Convert formats
util convert color "#ff0000" rgb        # rgb(255, 0, 0)
util convert color "0xFF5733" hsl       # hsl(10, 100%, 60%)
util convert base dec 255 bin           # 11111111
util convert base hex ff dec            # 255
util convert data 1048576 auto          # 1.00 MB
util convert time unix 1699564800 iso   # ISO timestamp
util convert config package.json yaml   # Output YAML
util convert file image.png image.jpg   # Convert images
util convert document README.md README.pdf  # Markdown to PDF
util convert text url-encode "hello world"  # hello%20world
util convert tabular data.csv json      # CSV to JSON

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

# Create test data
for i in {1..10}; do
  echo "$(util uuid),$(util lorem words --count 2),$(util random int --min 18 --max 80)"
done
```

## Convert Command Details

The `convert` command provides comprehensive format conversion capabilities:

### Color Conversions

Convert between hex, RGB, HSL, and integer formats:

```bash
util convert color "#ff0000" rgb      # → rgb(255, 0, 0)
util convert color "0xFF5733" hsl     # → hsl(10, 100%, 60%)
util convert color "rgb(255,0,0)" hex # → #ff0000
util convert color "#ff0000" int      # → 16711680
```

### Number Base Conversions

Convert between decimal, hexadecimal, binary, and octal:

```bash
util convert base dec 255 hex         # → ff
util convert base hex ff bin          # → 11111111
util convert base bin 11111111 dec    # → 255
util convert base dec 255 0x          # → 0xff
```

### Data Size Conversions

Convert between bytes, KB, MB, GB, TB with auto-detection:

```bash
util convert data 1048576 mb          # → 1.00 MB
util convert data 1.5GB kb            # → 1536.00 KB
util convert data 2048 auto           # → 2.00 KB
```

### Time Format Conversions

Convert between Unix timestamps and ISO format:

```bash
util convert time unix 1699564800 iso # → ISO timestamp
util convert time iso "2023-11-10T00:00:00" unix
util convert time unix 1699564800 date # → 2023-11-10
```

### Config File Conversions

Convert between JSON, YAML, TOML, and XML:

```bash
util convert config package.json yaml > package.yaml
util convert config settings.yaml toml > settings.toml
util convert config data.json xml > data.xml
```

### Text Encoding & Formatting

Convert text encodings and escape formats:

```bash
# URL encoding/decoding
util convert text url-encode "hello world"    # → hello%20world
util convert text url-decode "hello%20world"  # → hello world

# HTML entity encoding/decoding
util convert text html-encode "<div>Test</div>"  # → &lt;div&gt;Test&lt;/div&gt;
util convert text html-decode "&lt;div&gt;Test&lt;/div&gt;"  # → <div>Test</div>

# String escaping for programming languages
util convert text escape "It's test" --target sql       # → It''s test
util convert text escape "Line 1\nLine 2" --target python  # → Line 1\\nLine 2
util convert text unescape "It''s test" --target sql   # → It's test

# Line ending conversions
util convert text line-endings --file script.sh --target crlf  # Convert to Windows
util convert text line-endings --file script.sh --target lf    # Convert to Unix
```

### Tabular Data Conversions

Convert between CSV, JSON, and Markdown tables:

```bash
# CSV to JSON
util convert tabular data.csv json > data.json

# JSON to CSV
util convert tabular data.json csv > data.csv

# CSV to Markdown table
util convert tabular data.csv markdown > table.md

# JSON to Markdown table
util convert tabular products.json md > products_table.md

# Using alias 'table'
util convert table data.csv json
```

### Image/Video File Conversions

Convert images (JPG, PNG, WEBP, GIF, BMP, etc.):

```bash
util convert file photo.png photo.jpg
util convert file logo.jpg logo.webp
```

Convert video/audio (requires FFmpeg):

```bash
util convert file video.mov video.mp4
util convert file audio.wav audio.mp3
```

### Document Conversions

Convert between 40+ document formats using Pandoc:

```bash
util convert document README.md README.html
util convert document notes.md notes.pdf      # Requires LaTeX
util convert document doc.md doc.docx
util convert document README.rst README.md
```

Supported formats: Markdown, HTML, PDF, DOCX, ODT, RTF, reStructuredText, AsciiDoc, EPUB, LaTeX, Jupyter notebooks, and more.

## Validate Command Details

The `validate` command provides comprehensive validation for various data formats and types.

### Syntax Validation

Validate syntax for JSON, YAML, TOML, XML, HTML, and CSS. Automatically detects if input is a file path or direct content:

```bash
# JSON validation
util validate syntax json '{"name":"test","value":123}'  # Direct content
util validate syntax json config.json                    # File (auto-detected)

# YAML validation
util validate syntax yaml 'key: value\nlist: [1,2,3]'
util validate syntax yaml settings.yaml

# TOML validation
util validate syntax toml '[section]\nkey = "value"'
util validate syntax toml Cargo.toml

# XML validation
util validate syntax xml '<root><item>test</item></root>'
util validate syntax xml document.xml

# HTML validation (tag matching)
util validate syntax html '<html><body><h1>Title</h1></body></html>'
util validate syntax html index.html

# CSS validation (brace matching)
util validate syntax css 'body { color: red; }'
util validate syntax css styles.css

# From stdin
cat package.json | util validate syntax json
```

### Email Validation

Validate email address format (RFC 5322 compliant):

```bash
util validate email "user@example.com"
util validate email "john.doe+tag@company.co.uk"
```

### URL Validation

Validate URL format and structure:

```bash
util validate url "https://example.com/path"
util validate url "http://localhost:8080/api"
util validate url "https://github.com/user/repo"
```

### IP Address Validation

Validate IPv4 and IPv6 addresses:

```bash
# Auto-detect version
util validate ip "192.168.1.1"
util validate ip "2001:db8::1"

# Explicit version
util validate ip "10.0.0.1" --version 4
util validate ip "::1" --version 6
```

### Credit Card Validation

Validate credit card numbers using the Luhn algorithm:

```bash
util validate card "4532015112830366"            # Visa
util validate card "5425-2334-3010-9903"         # Mastercard (with hyphens)
util validate card "4532 0151 1283 0366"         # With spaces
util validate cc "371449635398431"               # Using alias
```

Supports formats with spaces or hyphens. Tests validity using Luhn checksum algorithm.

### File Checksum Validation

Verify file integrity using cryptographic checksums:

```bash
# SHA256 (default)
util validate checksum file.zip abc123def456...

# Other algorithms
util validate checksum download.tar.gz <hash> --algorithm md5
util validate checksum package.rpm <hash> --algorithm sha1
util validate checksum image.iso <hash> --algorithm sha512

# Using alias
util validate hash file.bin <checksum>
```

Supported algorithms: MD5, SHA1, SHA224, SHA256, SHA384, SHA512

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
│       ├── hash.py
│       ├── lorem.py
│       ├── random.py
│       ├── token.py
│       ├── uuid.py
│       └── validate.py
└── tests/                   # Test suite (313 tests)
```

## Requirements

### Core Dependencies (auto-installed)

- Python 3.7+
- argcomplete - Shell autocompletion
- lorem-text - Lorem Ipsum generation
- Pillow - Image conversions
- PyYAML, tomli, tomli-w, xmltodict - Config file conversions

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
