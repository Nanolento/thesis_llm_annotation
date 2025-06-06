# duplicate_check.py
# Checks for duplicate comments and deletes duplicates

import json
import sys

def merge_dicts(dict1, dict2):
    """Merge two dictionaries, preferring non-null values and combining keys."""
    merged = dict1.copy()
    for key, value in dict2.items():
        if key not in merged or merged[key] in (None, "", [], {}):
            merged[key] = value
    return merged

def deduplicate_by_name(data):
    merged_data = {}
    for item in data:
        name = item.get("name")
        if name:
            if name not in merged_data:
                merged_data[name] = item
            else:
                merged_data[name] = merge_dicts(merged_data[name], item)
    return list(merged_data.values())

if len(sys.argv) < 3:
    print("Usage: [in file] [out file]")
    exit(1)

with open(sys.argv[1], "r") as f:
    print("Loading data")
    data = json.load(f)
    print("Dedup data")
    dedup_data = deduplicate_by_name(data)

with open(sys.argv[2], "w") as of:
    print("Saving")
    json.dump(dedup_data, of, indent=4)
