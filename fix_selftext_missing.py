# fix_selftext_missing.py
# Adds back selftext so link_annotations works.

import json
import sys

if len(sys.argv) < 3:
    print("Usage: [in file] [out file]")
    exit(1)

with open(sys.argv[1], "r") as f:
    data = json.load(f)
    for d in data:
        d["selftext"] = ""

with open(sys.argv[2], "w") as of:
    json.dump(data, of, indent=4)
