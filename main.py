"""Write the pre-rendered newspaper page to the contest output directory."""

import os
import shutil
from pathlib import Path


def main() -> None:
    image = Path(__file__).resolve().with_name("entry.png")
    output = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(image, output / image.name)


if __name__ == "__main__":
    main()
