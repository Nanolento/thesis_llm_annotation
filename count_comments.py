# count_comments.py
# Counts the amount of comments in a dataset

import json
import sys

def count_comments(c):
    count = 0
    for ci in c:
        count += 1
        if "comments" in ci:
            subcount = count_comments(ci["comments"])
            count += subcount
        if "children" in ci:
            subcount = count_comments(ci["children"])
            count += subcount
    return count


if len(sys.argv) < 3:
    print("Usage: [in file] [method]\n"
          "In File: file to read and count comments from.\n"
          "Method: list or line, use list for JSON with list of dicts. use line for jsonl.")
    exit(1)

print("Loading data")
with open(sys.argv[1], "r") as f:
    if sys.argv[2] == "jsonl":
        data = f.readlines()
    else:
        data = json.load(f)

children_count = 0
data_size = len(data)
posts_done = 0
for l in data:
    if sys.argv[2] == "jsonl":
        j = json.loads(l)
    else:
        j = l
    if "comments" in j:
        children_count += count_comments(j["comments"])
    posts_done += 1
    print(f"Post {posts_done} / {data_size} posts -> {children_count} comments so far counted", end="\r")

print(f"\n{str(posts_done + children_count)} total posts/comments found")
