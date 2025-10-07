import sys
import argparse
import uuid

def uuid_v1_command(args):
    print(uuid.uuid1())

def uuid_v3_command(args):
    if not args.name or not args.namespace:
        print("Error: --name and --namespace are required for UUIDv3.")
        return
    try:
        namespace_uuid = uuid.UUID(args.namespace)
        print(uuid.uuid3(namespace_uuid, args.name))
    except ValueError:
        print(f"Error: Invalid namespace UUID '{args.namespace}'")
        sys.exit(1)

def uuid_v4_command(args):
    print(uuid.uuid4())

def uuid_v5_command(args):
    if not args.name or not args.namespace:
        print("Error: --name and --namespace are required for UUIDv5.")
        return
    try:
        namespace_uuid = uuid.UUID(args.namespace)
        print(uuid.uuid5(namespace_uuid, args.name))
    except ValueError:
        print(f"Error: Invalid namespace UUID '{args.namespace}'")
        sys.exit(1)

def setup_parser(subparsers):
    uuid_parser = subparsers.add_parser('uuid', help='Generate UUIDs', description='Generate various types of Universally Unique Identifiers (UUIDs).')
    uuid_subparsers = uuid_parser.add_subparsers(dest='version_command', help='UUID versions')

    # UUID v1
    v1_parser = uuid_subparsers.add_parser('v1', help='Generate a UUID version 1', description='Generate a time-based UUID (version 1).')
    v1_parser.set_defaults(func=uuid_v1_command)

    # UUID v3
    v3_parser = uuid_subparsers.add_parser('v3', help='Generate a UUID version 3 (name-based, MD5 hash)', description='Generate a name-based UUID (version 3) using MD5 hashing.')
    v3_parser.add_argument('--name', required=True, help='Name for UUIDv3')
    v3_parser.add_argument('--namespace', required=True, help='Namespace UUID for UUIDv3 (e.g., a valid UUID string)')
    v3_parser.set_defaults(func=uuid_v3_command)

    # UUID v4 (default)
    v4_parser = uuid_subparsers.add_parser('v4', help='Generate a UUID version 4 (random)', description='Generate a randomly generated UUID (version 4).')
    v4_parser.set_defaults(func=uuid_v4_command)

    # UUID v5
    v5_parser = uuid_subparsers.add_parser('v5', help='Generate a UUID version 5 (name-based, SHA-1 hash)', description='Generate a name-based UUID (version 5) using SHA-1 hashing.')
    v5_parser.add_argument('--name', required=True, help='Name for UUIDv5')
    v5_parser.add_argument('--namespace', required=True, help='Namespace UUID for UUIDv5 (e.g., a valid UUID string)')
    v5_parser.set_defaults(func=uuid_v5_command)

    # Set default function for 'uuid' if no subcommand is given (defaults to v4)
    uuid_parser.set_defaults(func=uuid_v4_command)