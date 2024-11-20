from pathlib import Path
from config import config

def generate_preface(file_path: Path):
    block = ""
    block += (
        f"[<< Table of Contents](../{'../' * (len(file_path.parts) -2)}index.md)\n\n"
    )
    block += f"# AI Generated documentation for `{config.project_name}/{file_path}`\n"
    block += "---\n"

    return block
