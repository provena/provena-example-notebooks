import json

def pprint_json(content) -> None:
    print(json.dumps(content,indent=2))