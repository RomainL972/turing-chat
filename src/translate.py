import yaml
import os

data = {}

def loadMessages(language="fr"):
    global data

    script_dir = os.path.dirname(__file__)
    rel_path = "translations/" + language + ".yaml"

    with open(os.path.join(script_dir, rel_path), 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def getMessage(data, keys):
    if isinstance(data, str):
        return data
    key = keys.pop(0)
    return getMessage(data[key], keys)

def tr(message):
    keys = message.split(".")
    return getMessage(data, keys)

loadMessages()
