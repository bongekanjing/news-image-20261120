#!/usr/bin/env python3
"""Copy the front-page image to the output directory (pure stdlib)."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
out = os.environ["MAKEFUN_OUTPUT_DIR"]
os.makedirs(out, exist_ok=True)
shutil.copyfile(os.path.join(here, "entry.png"),
                os.path.join(out, "entry.png"))
