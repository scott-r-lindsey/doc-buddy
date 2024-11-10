# doc-buddy

`doc-buddy` is a Python-based CLI tool for automatically generating documentation for your project files using OpenAI's API. The tool can process individual files or recursively document all files in a directory based on specified file types. This project is managed using [Poetry](https://python-poetry.org/), and the entry point is a bash script named `doc-buddy` located at the root of the repository.

## Features

- **File Documentation**: Point `doc-buddy` to a specific file and it will generate a documentation file with a `-apidoc.md` suffix next to it.
- **Recursive Directory Documentation**: Point `doc-buddy` to a directory, specify the file types to process, and it will document all matching files recursively.
- **Dry-run Mode**: Optionally preview the files to be processed without generating documentation.
- **Automatic Poetry Installation**: The `doc-buddy` bash script will attempt to install Poetry and run `poetry install` if it's not already installed.
- **Repository Root Context**: Users are expected to run `doc-buddy` from the root of the repository, as the path to the files is meaningful in the documentation.

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API credentials (set in a `.env` file)
- [Poetry](https://python-poetry.org/) for dependency management 

### Setup

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/scott-r-lindsey/doc-buddy
   cd doc-buddy
   ```

2. The `doc-buddy` bash script will automatically attempt to install [Poetry](https://python-poetry.org/) and the project dependencies for you. Just make sure you have `curl` installed for Poetry installation:

   ```bash
   ./doc-buddy
   ```

3. Set up your `.env` file in the project root directory with your OpenAI credentials:

  - Copy the .env.dist file to .env:

  ```bash
  cp .env.dist .env
  ```

- Fill in the .env file with your OpenAI credentials, or configure your Ollama or other provider's details.

### Adding `doc-buddy` to your PATH

To make `doc-buddy` available globally on your system without needing to be in the project directory, you can add it to your `PATH`. Here’s how:

1. Navigate to the root of the repository where the `doc-buddy` script is located.

2. Add the project directory to your `PATH` by appending the following line to your shell profile file (e.g., `.bashrc`, `.zshrc`, or `.profile`):

   ```bash
   export PATH="/path/to/doc-buddy/repo:$PATH"
   ```

   Replace `/path/to/doc-buddy/repo` with the actual path to the directory where `doc-buddy` resides.

3. Reload your shell configuration by running:

   ```bash
   source ~/.bashrc  # or source ~/.zshrc, depending on your shell
   ```

Once this is done, you can run `doc-buddy` from anywhere on your system:

```bash
doc-buddy /path/to/file.js /path/to/docs/folder/
```

## Usage

Before running `doc-buddy`, make sure you are at the root of your repository, as the file paths are meaningful for generating accurate documentation.

### Documenting a Single File

To document a single file:

```bash
doc-buddy ./some-file.py ./docs
```

This will generate the documentation in a new file n the folder `docs`, with the suffix `.md` (e.g., `some-file.js.md`).

### Documenting a Directory

To document all files of certain types within a directory:

```bash
cd my-repo
doc-buddy ./ ./docs --file-types py js jsx
```

This will process all `.py`, `.js`, and `.jsx` files recursively in the directory and generate corresponding markdown files in the `docs` folder.

### Dry Run

To perform a dry run (i.e., preview the files that would be processed):

```bash
cd my-repo
doc-buddy ./ ./docs --file-types py js jsx --dry-run
```

This will list the files that would have been documented without actually generating any documentation.

## Doc-Buddy generated Documentation for Doc-Buddy

Naturally, the code for doc-buddy has been documented with doc-buddy in the [docs folder](./docs/index.md).

## Contributing

If you'd like to contribute to `doc-buddy`, feel free to submit a pull request!

