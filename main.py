#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Entry program for the-picture-that-tastes-of-one: one beef burger.

Regenerates the picture with build_image.py (deterministic Pillow render,
no network, standard library plus Pillow only) and writes the result as
entry.png into the output directory: $MAKEFUN_OUTPUT_DIR when set,
otherwise /output. Running it twice writes identical bytes.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    subprocess.run(
        [sys.executable, str(HERE / "build_image.py")],
        cwd=HERE,
        check=True,
    )
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")


if __name__ == "__main__":
    main()
