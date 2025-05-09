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
As output, provide only the annotations in the format described below.

FORMAT OF OUTPUT
Please only provide your annotations in a "Element: Annotation" format, like in the below example.
Story: yes
Suspense: 3
Curiosity: 2
Surprise: 4
Note that this is an example, replace the given values above with your own annotations.
"""

def main():
    data = {
        "model": "llama3.2",
        "prompt": "Are you ready to do some awesome annotation work based on reader's perception?",
        "system": SYSTEM_PROMPT,
        "stream": False
    }
    response = requests.post(API_URL + "generate", json=data)
    if response.status_code == 400:
        print("Bad request:", response.text)
        return
    output = json.loads(response.text)
    print("Response by LLM:", output["response"])
    

if __name__ == "__main__":
    main()
