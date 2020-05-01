import os
import csv


class TrustManager():
    def __init__(self, printMessage, trustFile="trust.txt"):
        self.printMessage = printMessage
        self.trustFile = trustFile
        self.currentFingerprint = None
        self.currentUsername = None
        self.trusted = False
        self.forceTrusted = False
        self.savedFingerprints = self.getSavedFingerprints()

    def setCurrentFingerprint(self, fingerprint):
        self.currentFingerprint = fingerprint
        self.checkTrust()

    def getSavedFingerprints(self):
        parsedLines = {}
        if os.path.isfile(self.trustFile):
            with open(self.trustFile, "r") as f:
                lines = [line.rstrip('\n') for line in f]
                for line in lines:
                    parsed = line.split(",")
                    parsedLines[parsed[0]] = {"level": parsed[1]}
        return parsedLines

    def saveFingerprints(self):
        with open(self.trustFile, "w") as f:
            for fingerprint,entry in self.savedFingerprints.items():
                f.write(fingerprint + "," + entry["level"] + "\n")

    def checkTrust(self):
        if not self.currentFingerprint or self.forceTrusted:
            return
        if self.savedFingerprints and self.currentFingerprint in self.savedFingerprints:
            entry = self.savedFingerprints[self.currentFingerprint]
            if entry["level"] == "always":
                self.trusted = True
            elif entry["level"] == "never":
                self.trusted = False
        else:
            self.printMessage("Fingerprint inconnue " + self.currentFingerprint)
            self.printMessage("Utilisez /trust pour choisir un niveau de confiance")

    def setTrust(self, level):
        level = int(level)
        if not self.currentFingerprint:
            return
        if level < 0 or level > 2:
            raise ValueError
        if level == 0:
            entry = {}
            if self.savedFingerprints and self.currentFingerprint in self.savedFingerprints:
                entry = self.savedFingerprints[self.currentFingerprint]
            entry["level"] = "never"
            self.savedFingerprints[self.currentFingerprint] = entry
            self.saveFingerprints()
            self.trusted = False
            self.forceTrusted = False
            self.printMessage("Non-confiance enregistrée")
        elif level == 1 or level == 2:
            self.trusted = True
            self.forceTrusted = True
            if level == 2:
                entry = {}
                if self.savedFingerprints and self.currentFingerprint in self.savedFingerprints:
                    entry = self.savedFingerprints[self.currentFingerprint]
                entry["level"] = "always"
                self.savedFingerprints[self.currentFingerprint] = entry
                self.saveFingerprints()
            self.printMessage("Confiance enregistrée")

    def connexionTrusted(self):
        self.checkTrust()
        return self.trusted or self.forceTrusted
