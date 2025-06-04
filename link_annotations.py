# link_annotations.py
# Links annotations back into the original dataset, to be used for analysis
# Also deletes useless comments.

import sys
import json

if len(sys.argv) < 4:
    print("Usage: [data in] [annotations in] [out file]\n"
          "Data In: file containing dataset\n"
          "Annotations In: file containing annotations by LLM\n"
          "Out File: file path to save data with annotations added to")
    exit(1)

print("Loading data")
with open(sys.argv[1], "r") as df, open(sys.argv[2], "r") as af:
    annotations = json.load(af)
    data = json.load(df)

print("Building index")
# build index for faster lookup
index = {}
for idx, d in enumerate(data):
    index[d["name"]] = idx

invalid_comment_ids = set()
print("Linking")
for comment_id in annotations.keys():
    if comment_id in index:
        d_idx = index[comment_id]
        # add labels from annotation to dataset.
        data[d_idx].update(annotations[comment_id])
        # check if useful or not
        if (data[d_idx]["author"] == "[deleted]" or
            data[d_idx]["body"] == "[deleted]" or
            data[d_idx]["selftext"] == "[removed]" or
            data[d_idx]["body"] == ""):
            print(f"'{comment_id}' useless. Marking for removal.")
            invalid_comment_ids.add(comment_id) # remove useless comment.
    else:
        print(f"'{comment_id}' not in dataset! Not linking")

print("Removing marked comments")
data = [d for d in data if d.get("name") not in invalid_comment_ids and d.get("name") in annotations.keys()]
        
print("Saving out file")
with open(sys.argv[3], "w") as of:
    json.dump(data, of, indent=4)
