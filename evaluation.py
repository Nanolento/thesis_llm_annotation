# Evaluation.py
# This program will evaluate the LLM performance of annotation by comparing it to the
# original golden standard data

import json
import sys

from sklearn.metrics import (
    accuracy_score, precision_score,
    recall_score, f1_score
)


if len(sys.argv) < 3:
    print("Usage: <filename of annotation> <golden standard file>\n"
          "Please give the filenames for the files to check!")
    exit(1)

with open(sys.argv[1], "r") as af, open(sys.argv[2], "r") as gf:
    orig_data = json.load(gf)
    annotations = json.load(af)

    y_true = {
        "story": [],
        "suspense": [],
        "surprise": [],
        "curiosity": []
    }
    y_pred = {
        "story": [],
        "suspense": [],
        "surprise": [],
        "curiosity": []
    }
    for comment in orig_data:
        if comment["name"] not in annotations:
            print(comment["name"], "not in annotations.")
            continue
        annotation = annotations[comment["name"]]
        for cat in ["story", "suspense", "curiosity", "surprise"]:
            if cat == "story":
                val1 = comment["story_class"] == "Story"
                val2 = annotation["story"]
                y_pred["story"].append(val2)
                y_true["story"].append(val1)
            else:
                val1 = comment[cat]
                val2 = annotation[cat]
                y_pred[cat].append(val2)
                y_true[cat].append(val1)

            if val1 != val2:
                print(f"{cat} annotation mismatch for {comment['name']}.")

        
#print(f"Correct count: {correct_count['global']}/{len(annotations)*4}")
print("Total count:", len(annotations))
#print("Accuracy (global):", correct_count["global"] / (len(annotations) * 4))
for cat in ["story", "suspense", "curiosity", "surprise"]:
    yt = [l for l in y_true[cat]]
    yp = [l for l in y_pred[cat]]

    accuracy = accuracy_score(yt, yp)
    precision = precision_score(yt, yp, average="weighted", zero_division=0)
    recall = recall_score(yt, yp, average="weighted", zero_division=0)
    f1 = f1_score(yt, yp, average="macro", zero_division=0)
    f1w = f1_score(yt, yp, average="weighted", zero_division=0)
    print(f"Accuracy ({cat}): {accuracy}")
    print(f"Precision ({cat}): {precision}")
    print(f"Recall ({cat}): {recall}")
    print(f"F1-score ({cat}) (macro): {f1}")
    print(f"F1-score ({cat}) (weighted): {f1w}")
