#!/bin/bash

for i in 1 3 5 8 10; do
    rm eval_story.txt
    rm eval_suspense.txt
    rm eval_curiosity.txt
    rm eval_surprise.txt
    echo "==== Few-shot (${i} examples) ===="
    for r in {1..10}; do
        RUN_SCORES=$(python3 evaluation.py fewshot_annotations/att_few_${i}_run${r}.json data/golden-standard-test.json | grep "weighted" | cut -d ":" -f2 | cut -c2-)
        echo "$RUN_SCORES" | sed -n "1p" >> eval_story.txt
        echo "$RUN_SCORES" | sed -n "2p" >> eval_suspense.txt
        echo "$RUN_SCORES" | sed -n "3p" >> eval_curiosity.txt
        echo "$RUN_SCORES" | sed -n "4p" >> eval_surprise.txt
    done
    python3 parse_bulk_eval.py
done
