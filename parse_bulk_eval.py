# parse_bulk_eval.py
# This program reads output from the files created by evaluate_fewshot.sh
# and calculates means and stddev for the f1_scores.

import math

for cat in ["story", "suspense", "curiosity", "surprise"]:
    with open(f"eval_{cat}.txt") as f:
        score_lines = f.readlines()
        scores = [float(s) for s in score_lines]
        mean_f1 = sum(scores) / len(scores)
        variance = sum([(s - mean_f1) ** 2 for s in scores]) / len(scores)
        stddev = math.sqrt(variance)
        print(f"{cat} mean F1_score: {mean_f1}")
        print(f"{cat} std. dev.: {stddev}")
