# Project: cliutils - A Modular Command-Line Utility

## Project Overview

`cliutils` is a modular command-line utility (CLI) script designed to provide a collection of common terminal programs with autocompletion. It is built with Python and leverages `argparse` for robust command-line argument parsing and `argcomplete` for enhanced shell autocompletion. The project's architecture emphasizes modularity, allowing for easy extension and addition of new utility commands as separate Python modules without disrupting the core structure.

## Main Technologies

*   **Python**: The primary programming language for the CLI.
*   **`argparse`**: Python's standard library for parsing command-line arguments, enabling a structured and user-friendly interface.
*   **`argcomplete`**: A Python package that provides extensible tab completion for `argparse` applications, significantly improving the user experience.
*   **`pytest`**: A popular Python testing framework used for writing comprehensive and efficient tests.
*   **`lorem-text`**: A third-party Python library used for generating Lorem Ipsum text, demonstrating integration with external packages.

## Architecture

The `cliutils` project follows a clear and modular architecture to facilitate development and maintenance:

*   **`util/main.py`**: This is the central entry point of the CLI. It is responsible for:
    *   Setting up the main `argparse` parser.
    *   Dynamically discovering and loading individual command modules from the `util/commands/` directory.
    *   Dispatching command-line calls to the appropriate functions within each command module.
    *   Integrating `argcomplete` to provide shell autocompletion.

*   **`util/commands/`**: This directory serves as a container for all individual utility command modules. Each Python file within this directory represents a distinct command (e.g., `uuid.py`, `base64.py`, `lorem.py`, `completion.py`).
    *   Each command module is expected to define a `setup_parser` function. This function takes the main `argparse` subparsers object as an argument and registers its specific subcommands, arguments, and help messages.

*   **`setup.py`**: This file defines the `cliutils` Python package. It specifies metadata such as the project name, version, and dependencies. Crucially, it configures the `util` console script entry point, allowing the CLI to be invoked directly from the terminal after installation.

*   **`cli-util`**: A simple bash wrapper script located in the project root. Its purpose is to:
    *   Activate the Python virtual environment (if one exists and is configured).
    *   Execute the main Python CLI script (`python -m util.main`) with all passed arguments.
    This wrapper ensures that the CLI runs within the correct Python environment, regardless of how it's invoked.

## Building and Running

To set up and run the `cliutils` project, follow these steps:

1.  **Setup Virtual Environment (Recommended)**:
    It is highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install Dependencies**:
    Install the project in editable mode, which also installs all its specified dependencies (e.g., `argcomplete`, `lorem-text`).
    ```bash
    pip install -e .
    ```

3.  **Enable Autocompletion**:
    `argcomplete` provides powerful tab completion. Choose one of the following activation methods:

    *   **Global Activation (Recommended for general use)**:
        This command sets up `argcomplete` for all Python scripts in your environment that use it.
        ```bash
        activate-global-python-argcomplete
        ```
        After running this, refresh your shell environment (e.g., by opening a new terminal session or running `source ~/.bashrc` for Bash or `source ~/.zshrc` for Zsh).

    *   **Per-Application Activation (for specific scripts)**:
        If you prefer to enable completion only for `util`, add this line to your shell configuration file (`~/.bashrc` or `~/.zshrc`) for persistence:
        ```bash
        eval "$(register-python-argcomplete util)"
        ```

4.  **Run Commands**:
    Once installed and autocompletion is enabled, you can invoke the `util` command followed by its subcommands and arguments. For example:
    ```bash
    util uuid
    util uuid v1
    util uuid v3 --name myname --namespace 6ba7b810-9dad-11d1-80b4-00c04fd430c8
    util base64 encode "Hello World"
    util base64 decode "SGVsbG8gV29ybGQ="
    util lorem paragraphs 3
    util lorem p 2
    util lorem sentences 5
    util lorem s 10
    util lorem words 15
    util lorem w 20
    util completion bash
    ```

## Testing

The project utilizes `pytest` for its testing framework. All tests are located in the `tests/` directory.

To run all tests:
```bash
pytest
```

## Development Conventions

*   **Modularity**: New utility commands should be implemented as separate Python files within the `util/commands/` directory.
*   **`argparse` Integration**: Each new command module must define a `setup_parser(subparsers)` function. This function is responsible for adding the command's parser and its arguments to the main CLI parser.
*   **`setup_parser` Function**: This function is the standard interface for command modules to register themselves with the main `util` CLI.
*   **Error Handling**: Commands should use `sys.exit(1)` to indicate non-zero (failure) exit codes when errors occur, ensuring proper shell scripting behavior.
*   **Testing**: Every new command should be accompanied by a comprehensive set of `pytest` tests in the `tests/` directory. Tests should invoke the CLI commands as subprocesses to accurately simulate real-world usage and verify `stdout`, `stderr`, and `returncode`.
