from lorem_text import lorem as lt


def lorem_command(args):
    # Ensure args.type defaults to 'paragraphs' if not provided
    if args.type is None:
        args.type = "paragraphs"

    # Handle aliases
    if args.type in ["paragraphs", "p"]:
        text_list = lt.paragraphs(args.count)
        text = "\n\n".join(text_list)
    elif args.type in ["sentences", "s"]:
        # lorem_text.lorem.sentences does not exist, so we generate multiple sentences
        text_list = [lt.sentence() for _ in range(args.count)]
        text = " ".join(text_list)
    elif args.type in ["words", "w"]:
        text_list = lt.words(args.count)
        text = " ".join(text_list)
    else:
        # Should not happen due to argparse choices and default
        text = ""

    print(text)


def setup_parser(subparsers):
    lorem_parser = subparsers.add_parser(
        "lorem",
        help="Generate Lorem Ipsum text",
        description="Generate Lorem Ipsum text (paragraphs, sentences, or words).",
    )
    lorem_subparsers = lorem_parser.add_subparsers(
        dest="type", required=True, help="Type of Lorem Ipsum to generate"
    )

    # Paragraphs subcommand
    paragraphs_parser = lorem_subparsers.add_parser(
        "paragraphs",
        aliases=["p"],
        help="Generate paragraphs",
        description="Generate Lorem Ipsum paragraphs.",
    )
    paragraphs_parser.add_argument(
        "--count", type=int, default=1, help="Number of paragraphs to generate"
    )
    paragraphs_parser.set_defaults(func=lorem_command)

    # Sentences subcommand
    sentences_parser = lorem_subparsers.add_parser(
        "sentences",
        aliases=["s"],
        help="Generate sentences",
        description="Generate Lorem Ipsum sentences.",
    )
    sentences_parser.add_argument(
        "--count", type=int, default=1, help="Number of sentences to generate"
    )
    sentences_parser.set_defaults(func=lorem_command)

    # Words subcommand
    words_parser = lorem_subparsers.add_parser(
        "words",
        aliases=["w"],
        help="Generate words",
        description="Generate Lorem Ipsum words.",
    )
    words_parser.add_argument(
        "--count", type=int, default=1, help="Number of words to generate"
    )
    words_parser.set_defaults(func=lorem_command)
