import json

with open("settings.json","r") as file:
    setting_params = file.read()

settings = json.loads(setting_params)

def update_setting(setting,new_value):
    settings[setting] = new_value
    with open("settings.json","w") as output:
        json.dump(settings, output)