# data_combiner.py
# Merges two comment datasets together.
# Useful for combining the regular annotated dataset and annotated converted selftext datasets together
# This script can theoretically combine any two files with a list of dicts together

import json
import sys

if len(sys.argv) < 4:
    print("Usage: [in1 file] [in2 file] [out file]")
    exit(1)

with open(sys.argv[1], "r") as f1, open(sys.argv[2], "r") as f2:
    data1 = json.load(f1)
    data2 = json.load(f2)
    data_combined = data1 + data2

with open(sys.argv[3], "w") as of:
    json.dump(data_combined, of, indent=4)
