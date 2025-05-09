# Main.py
# This file will ask a running Ollama instance questions about the discussions
# and make it annotate stuff.

import requests
import json

api_url = "http://localhost:11434/api/"

def main():
    data = {
        "model": "llama3.2",
        "prompt": "Are you ready to do some awesome annotation work based on reader's perception?",
        "stream": False
    }
    response = requests.post(api_url + "generate", json=data)
    if response.status_code == 400:
        print("Bad request:", response.text)
        return
    output = json.loads(response.text)
    print("Response by LLM:", output["response"])
    

if __name__ == "__main__":
    main()
