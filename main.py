#!/usr/bin/env python3
"""Copy the front-page image to the output directory (pure stdlib).

The entry is a newspaper front page summing up the world news of
Friday 20 November 2026. The program runs with no network and must
write exactly the same bytes on every run, so it only copies the
entry.png that ships in this repository.
"""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "entry.png")
if not os.path.isfile(src):
    raise SystemExit("entry.png missing next to main.py")
out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out, exist_ok=True)
shutil.copyfile(src, os.path.join(out, "entry.png"))
