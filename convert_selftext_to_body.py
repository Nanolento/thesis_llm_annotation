# convert_selftext_to_body.py
# Convert comments with empty body and selftext to have the body be the selftext.

import json
import sys

if len(sys.argv) < 3:
    print("Usage: [in file] [out file]")
    exit(1)

with open(sys.argv[1], "r") as f:
    data = json.load(f)

new_data = []
for comment in data:
    if comment["body"] == "" and comment["selftext"]:
        new_comment = comment.copy()
        new_comment["body"] = new_comment["selftext"]
        del new_comment["selftext"]
        new_data.append(new_comment)

with open(sys.argv[2], "w") as f:
    print(len(new_data), "comments had selftext instead of body.")
    json.dump(new_data, f, indent=4)
