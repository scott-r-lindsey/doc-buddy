import os
from config import config


def add_readme():
    readme_path = config.docbuddy_root_path / "fixture" / "markdown-explanation"

    # read that file
    with open(readme_path, "r", encoding="utf-8") as file:
        readme = file.read()

    # write that file to config.output_path / 'README.txt'
    with open(config.output_path / "README.txt", "w", encoding="utf-8") as file:
        file.write(readme)
