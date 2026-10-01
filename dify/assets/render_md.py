import json

def main(text):
    parsed = json.loads(text)
    return { "result": parsed["text"] }
