# Main.py
# This file will ask a running Ollama instance questions about the discussions
# and make it annotate stuff.

import requests
import json

API_URL = "http://localhost:11434/api/"
SYSTEM_PROMPT = """
You are an annotator of reader's perception and narrative detection. Your goal is to
annotate Reddit comments from r/ChangeMyView. You will be provided Reddit comments and posts (hereafter passages)
to annotate on reader's perception.

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
    with open("data/golden-standard-train.json", "r") as f:
        comments = json.load(f)

    annotations = {}
    for comment in comments[:100]:
        # Put comment text in as prompt
        data["prompt"] = comment["body"]
        annotations[comment["name"]] = {}
        # Get response from LLM
        response = requests.post(API_URL + "generate", json=data)
        if response.status_code == 400:
            print("Bad request:", response.text)
            return
        # Parse output
        output = json.loads(response.text)
        print(f"\nPassage ID = {comment['name']}\n{output['response']}")
        try:
            for line in output["response"].split("\n"):
                line2 = line.split(":")
                prop = line2[0].lower()
                val = line2[1].lstrip() # Remove leading space.
                if prop == "story":
                    annotations[comment["name"]][prop] = val == "yes" # convert yes/no to true/false
                else:
                    annotations[comment["name"]][prop] = int(val)
        except (IndexError, ValueError):
            print("Broken annotation, ignoring.")
            if comment["name"] in annotations:
                del annotations[comment["name"]]
            continue

    # Save output
    with open("annotations.json", "w") as f:
        print("Saving output")
        json.dump(annotations, f)


if __name__ == "__main__":
    main()
