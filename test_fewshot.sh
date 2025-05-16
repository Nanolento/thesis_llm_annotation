#!/bin/bash

for i in 1 3 5 8 10; do
    for r in {1..10}; do
        python3 main.py data/golden-standard-test.json fewshot fewshot_annotations/att_few_${i}_run${r}.json ${i}
        python3 validate_annotations.py fewshot_annotations/att_few_${i}_run${r}.json
    done
done
