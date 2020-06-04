import yaml
import os


class Translate():
    def __init__(self, printMessage, language):
        self.printMessage = printMessage
        self.language = language
        self.messages = {}
        self.loadTranslations()

    def loadTranslations(self):
        script_dir = os.path.dirname(__file__)
        rel_path = "translations/" + self.language + ".yaml"

        with open(os.path.join(script_dir, rel_path), 'r') as stream:
            try:
                self.messages = yaml.safe_load(stream)
            except yaml.YAMLError:
                self.printMessage("error.yaml")

    def getMessage(self, data, keys):
        if isinstance(data, str):
            return data
        key = keys.pop(0)
        return self.getMessage(data[key], keys)

    def tr(self, message):
        keys = message.split(".")
        return self.getMessage(self.messages, keys)

    def setLanguage(self, language):
        self.language = language
        self.loadTranslations()


translate = None


def setObject(object):
    global translate
    translate = object


def tr(message):
    if translate:
        return translate.tr(message)
    return ""
