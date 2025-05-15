# Evaluation.py
# This program will evaluate the LLM performance of annotation by comparing it to the
# original golden standard data

import json
import sys


if len(sys.argv) < 3:
    print("Usage: <filename of annotation> <golden standard file>\n"
          "Please give the filenames for the files to check!")
    exit(1)

with open(sys.argv[1], "r") as af, open(sys.argv[2], "r") as gf:
    orig_data = json.load(gf)
    annotations = json.load(af)

    correct_count = {
        "global": 0,
        "story": 0,
        "suspense": 0,
        "curiosity": 0,
        "surprise": 0
    }
    for comment in orig_data:
        if comment["name"] not in annotations:
            print(comment["name"], "not in annotations.")
            continue
        annotation = annotations[comment["name"]]
        good = True
        for cat in ["story", "suspense", "curiosity", "surprise"]:
            if cat == "story":
                val1 = comment["story_class"] == "Story"
                val2 = annotation["story"]
            else:
                val1 = comment[cat]
                val2 = annotation[cat]

            if val1 != val2:
                print(f"{cat} annotation mismatch for {comment['name']}.")
                good = False
            else:
                correct_count[cat] += 1
        print(f"{comment['name']} is {'correct' if good else 'not correct'}")
        if good:
            correct_count["global"] += 1
        
print("Correct count:", correct_count["global"])
print("Total count:", len(annotations))
print("Accuracy (global):", correct_count["global"] / len(annotations))
for cat in ["story", "suspense", "curiosity", "surprise"]:
    print(f"Accuracy ({cat}): {correct_count[cat]}/{len(annotations)} -> {correct_count[cat] / len(annotations)}")
