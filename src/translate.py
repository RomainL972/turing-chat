import yaml

with open("translations/fr.yaml", 'r') as stream:
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
