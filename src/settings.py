import os
import yaml


class Settings():
    def __init__(self, printMessage):
        self.settingsFile = "settings.yaml"
        self.printMessage = printMessage
        self.settings = self.getSettingsFile()
        if not self.settings:
            self.settings = self.getDefaultSettings()
            self.saveSettings()

    def getDefaultSettings(self):
        return {
            "username": "User",
            "language": "fr",
            "lastHost": "127.0.0.1"
        }

    def getSettingsFile(self):
        if os.path.isfile(self.settingsFile):
            with open(self.settingsFile, "r") as f:
                try:
                    return yaml.safe_load(f)
                except yaml.YAMLError as exc:
                    self.printMessage(exc)
        return None

    def setSetting(self, setting, value):
        self.settings[setting] = value
        self.saveSettings()

    def getSetting(self, setting):
        try:
            return self.settings[setting]
        except KeyError:
            return self.getDefaultSettings()[setting]

    def saveSettings(self):
        with open(self.settingsFile, "w") as f:
            try:
                yaml.safe_dump(self.settings, f)
            except yaml.YAMLError as exc:
                self.printMessage(exc)
