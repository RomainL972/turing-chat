settingsDefaults = {
    "username": "User",
}


def get(name):
    return settingsDefaults.get(name)
