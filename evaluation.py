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

    # Used for calculating accuracy and precision
    correct_count = {
        "global": 0,
        "story": 0,
        "suspense": 0,
        "curiosity": 0,
        "surprise": 0
    }
    # The below dictionary is used for calculating recall
    # !! only applicable to Likert scale annotations.
    # 'model': has the model annotated X when it should have been X?
    # 'gold': should it have been X?
    class_correct = {}
    for comment in orig_data:
        if comment["name"] not in annotations:
            print(comment["name"], "not in annotations.")
            continue
        annotation = annotations[comment["name"]]
        for cat in ["story", "suspense", "curiosity", "surprise"]:
            if cat == "story":
                val1 = comment["story_class"] == "Story"
                if "story" not in class_correct:
                    class_correct["story"] = {
                        "gold": 0,
                        "model": 0
                    }
                if val1:
                    class_correct["story"]["gold"] += 1
                
                val2 = annotation["story"]
            else:
                val1 = comment[cat]
                if cat not in class_correct:
                    class_correct[cat] = {}
                if val1 not in class_correct[cat]:
                    class_correct[cat][val1] = {
                        "gold": 1,
                        "model": 0
                    }
                else:
                    class_correct[cat][val1]["gold"] += 1
                val2 = annotation[cat]

            if val1 != val2:
                print(f"{cat} annotation mismatch for {comment['name']}.")
            else:
                correct_count[cat] += 1
                correct_count["global"] += 1
                if cat != "story":
                    class_correct[cat][val2]["model"] += 1
                elif val1 and val2:
                    class_correct[cat]["model"] += 1

        
print(f"Correct count: {correct_count['global']}/{len(annotations)*4}")
print("Total count:", len(annotations))
print("Accuracy (global):", correct_count["global"] / (len(annotations) * 4))
for cat in ["story", "suspense", "curiosity", "surprise"]:
    # precision = correct_count[cat]
    # precision is "voor alle keren dat het model 4 annotate, hoe vaak klopte dat?"
    # recall is "voor alle keren als 4 geannotate, hoe vaak deed het model dat ook?"
    precision = correct_count[cat] / len(annotations)
    if cat != "story":
        recalls = {}
        for i in range(1,6):
            if i not in class_correct[cat]:
                print(i, "not in", cat, "so ignoring")
                continue
            recalls[i] = class_correct[cat][i]["model"] / class_correct[cat][i]["gold"]
        recall = sum(recalls.values()) / len(recalls)
    else:
        recall = class_correct["story"]["model"] / class_correct["story"]["gold"]
    f1_score = 2 * ((precision * recall) / (precision + recall))
    print(f"Accuracy ({cat}): {correct_count[cat]}/{len(annotations)} -> {correct_count[cat] / len(annotations)}")
    print(f"Precision ({cat}): {precision}")
    print(f"Recall ({cat}): {recall}")
    print(f"F1-score ({cat}): {f1_score}")
    
