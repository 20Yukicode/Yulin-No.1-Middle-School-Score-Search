import json


def readJsonFile(path: str):
    with open(path) as f:
        jsonResult = json.load(f)
        return jsonResult
