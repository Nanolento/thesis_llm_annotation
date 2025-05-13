# Main.py
# This file will ask a running Ollama instance questions about the discussions
# and make it annotate stuff.

import requests
import json
import time
import sys
import os
import random

API_URL = "http://localhost:11434/api/"
SYSTEM_PROMPT = """
You are an annotator of reader's perception and narrative detection. Your goal is to
annotate Reddit comments from r/ChangeMyView. You will be provided Reddit comments and posts (hereafter passages)
to annotate on reader's perception.
You are annotating for academic research purposes. The annotations will be used to do statistical analysis on
persuasion based on reader's perception. Please do not worry about potentially emotionally charged passages you see,
please annotate them as usual.

INPUT
You will receive passages as text. You should base your annotation off of the reader's perception of this text.

METHOD
You will annotate these passages on these reader's perception elements: suspense, curiosity and surprise. Each
of these should be annotated on a Likert scale from 1 to 5. You will also annotate the passage on if it
has a story or contains a narrative or not. This is a binary class which you should annotate as yes or no.

OUTPUT
As output, provide only the annotations in the format described below. Only use the categories "Story", "Suspense",
"Curiosity" and "Surprise". Do not use any other categories, only annotate these ones.

FORMAT OF OUTPUT
Please only provide your annotations in a "Element: Annotation" format, like in the below example. Do not put "Element:" in front
of the annotation, just the category followed by a colon and a space and then the annotation you created.
Story: yes
Suspense: 3
Curiosity: 2
Surprise: 4
Note that this is an example, replace the given values above with your own annotations.
"""


def main():
    data = {
        "model": "llama3.2",
        "system": SYSTEM_PROMPT,
        "stream": False
    }
    if len(sys.argv) < 2:
        print("Usage: python main.py <in file> <method> <out file>")
        print("In-File: file to load for model to annotate.\n"
              "Out-File: file to save annotations in (should be .json)\n"
              "Method: either 'zeroshot' or 'fewshot'")
        return
    print("Loading file for passages to annotate")
    if not os.path.isfile(sys.argv[1]):
        print("File does not exist!")
        return
    with open(sys.argv[1], "r") as f:
        comments = json.load(f)

    method = "fewshot" if len(sys.argv) >= 3 and sys.argv[2] == "fewshot" else "zeroshot"
    print(f"Using method {method}")
    start_time = time.time()
    annotations = {}
    if method == "fewshot":
        print("Loading file for fewshot examples")
        with open("data/golden-standard-train.json", "r") as f:
            examples = json.load(f)
        
    for comment in comments:
        # Put comment text in as prompt
        if method == "zeroshot":
            data["prompt"] = comment["body"]
        elif method == "fewshot":
            data["prompt"] = "EXAMPLE ANNOTATIONS\n"
            for _ in range(3):
                example_id = random.randint(0, len(examples))
                data["prompt"] += "Passage: " + examples[example_id]["body"] + "\n"
                data["prompt"] += "Story: "
                data["prompt"] += "yes" if examples[example_id]["story_class"] == "Story" else "no"
                data["prompt"] += "\nSuspense: " + str(examples[example_id]["suspense"])
                data["prompt"] += "\nCuriosity: " + str(examples[example_id]["curiosity"])
                data["prompt"] += "\nSurprise: " + str(examples[example_id]["surprise"]) + "\n\n"
            data["prompt"] += "\n\nPASSAGE TO ANNOTATE\n"
            data["prompt"] += "Passage: " + comment["body"]
        annotations[comment["name"]] = {}
        # Get response from LLM
        print("\nPrompt given to LLM:", data["prompt"])

        try:
            response = requests.post(API_URL + "generate", json=data)
            if response.status_code == 400:
                print("Bad request:", response.text)
                return
        except requests.exceptions.ConnectionError:
            print("Could not connect to Ollama! Is it running?")
            return
        # Parse output
        output = json.loads(response.text)
        print(f"\nPassage ID = {comment['name']}\n{output['response']}")
        try:
            for line in output["response"].split("\n"):
                line2 = line.split(":")
                if len(line) < 2:
                    # the model has put text other than annotations probably. ignore.
                    continue
                prop = line2[0].lower()
                val = line2[1].lstrip() # Remove leading space.
                # Now we put it in the annotations dict.
                # The reason we are checking the prop name is because the LLM
                # sometimes puts things in front of the category like "Element:"
                # or "1)".
                if "story" in prop:
                    annotations[comment["name"]]["story"] = val == "yes" # convert yes/no to true/false
                elif "suspense" in prop:
                    annotations[comment["name"]]["suspense"] = int(val)
                elif "surprise" in prop:
                    annotations[comment["name"]]["surprise"] = int(val)
                elif "curiosity" in prop:
                    annotations[comment["name"]]["curiosity"] = int(val)
                else:
                    print(f"Unknown category {prop}")
        except (IndexError, ValueError):
            print("Broken annotation, ignoring.")
            if comment["name"] in annotations:
                del annotations[comment["name"]]
            continue

    # Save output
    if len(sys.argv) >= 4:
        out_file_path = sys.argv[3]
    else:
        out_file_path = "annotations.json"
    with open(out_file_path, "w") as f:
        print(f"Saving output to {out_file_path}")
        print(f"That is {len(annotations)} annotations done in {time.time() - start_time} seconds.")
        json.dump(annotations, f)


if __name__ == "__main__":
    main()
