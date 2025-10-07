import argparse
import base64
import sys

def base64_encode_command(args):
    encoded_bytes = base64.b64encode(args.input_string.encode('utf-8'))
    print(encoded_bytes.decode('utf-8'))

def base64_decode_command(args):
    try:
        decoded_bytes = base64.b64decode(args.input_string.encode('utf-8'))
        print(decoded_bytes.decode('utf-8'))
    except base64.binascii.Error:
        print("Error: Invalid base64 string.")
        sys.exit(1)
    except UnicodeDecodeError:
        print("Error: Could not decode base64 output to UTF-8. The input might not be valid UTF-8 after decoding.")
        sys.exit(1)

def setup_parser(subparsers):
    base64_parser = subparsers.add_parser('base64', help='Encode or decode base64', description='Encode or decode strings using Base64.')
    base64_subparsers = base64_parser.add_subparsers(dest='action', help='Base64 actions')

    # Encode subcommand
    encode_parser = base64_subparsers.add_parser('encode', help='Encode a string to base64', description='Encodes the given string to Base64.')
    encode_parser.add_argument('input_string', help='The string to encode')
    encode_parser.set_defaults(func=base64_encode_command)

    # Decode subcommand
    decode_parser = base64_subparsers.add_parser('decode', help='Decode a base64 string', description='Decodes the given Base64 string.')
    decode_parser.add_argument('input_string', help='The base64 string to decode')
    decode_parser.set_defaults(func=base64_decode_command)
