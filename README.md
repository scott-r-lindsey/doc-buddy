# Doc Buddy

`Doc Buddy` is a Python-based CLI tool for automatically generating documentation for your project files using OpenAI's API. The tool can process individual files or recursively document all files in a directory based on specified file types. This project is managed using [Poetry](https://python-poetry.org/), and the entry point is a bash script named `doc-buddy` located at the root of the repository.

## Features

- **File Documentation**: Point `Doc Buddy` to a specific file and it will generate a documentation file with a `-apidoc.md` suffix next to it.
- **Recursive Directory Documentation**: Point `Doc Buddy` to a directory, specify the file types to process, and it will document all matching files recursively.
- **Dry-run Mode**: Optionally preview the files to be processed without generating documentation.
- **Poetry Management**: The project dependencies and environment are managed via Poetry for easy setup and management.

## Installation

### Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/docs/#installation) for managing dependencies
- OpenAI API credentials (set in a `.env` file)

### Setup

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/doc-buddy.git
   cd doc-buddy
   ```

2. Install the project dependencies using Poetry:

   ```bash
   poetry install
   ```

3. Set up your `.env` file in the project root directory with your OpenAI credentials:

   ```bash
   OPENAI_API_KEY=your-api-key-here
   USER_CWD=/path/to/your/project
   ```

## Usage

The main entry point is a bash script named `doc-buddy`, which you can use to document files or directories.

### Documenting a Single File

To document a single file:

```bash
./doc-buddy /path/to/file.js
```

This will generate the documentation in a new file next to the target file, with the suffix `-apidoc.md` (e.g., `file.js-apidoc.md`).

### Documenting a Directory

To document all files of certain types within a directory:

```bash
./doc-buddy /path/to/directory --file-types py js jsx
```

This will process all `.py`, `.js`, and `.jsx` files recursively in the directory and generate corresponding `-apidoc.md` files.

### Dry Run

To perform a dry run (i.e., preview the files that would be processed):

```bash
./doc-buddy /path/to/directory --file-types py js jsx --dry-run
```

This will list the files that would have been documented without actually generating any documentation.

## Project Structure

- `doc-buddy`: The bash script entry point for the project.
- `ai.py`: Contains the functions for interacting with the OpenAI API.
- `util.py`: Utility functions, such as reading files and getting absolute paths.
- `.env`: Environment variables file (not included in the repo, needs to be created).
- `README.md`: This file.

## Bash Script (`doc-buddy`)

Here’s a basic example of what your `doc-buddy` script might look like:

```bash
#!/bin/bash
poetry run python -m doc_buddy "$@"
```

Make sure to give it execution permissions:

```bash
chmod +x doc-buddy
```

## Development

1. To activate the Poetry shell:

   ```bash
   poetry shell
   ```

2. To run the tests:

   ```bash
   poetry run pytest
   ```

## Contributing

If you'd like to contribute to `Doc Buddy`, feel free to submit a pull request!

