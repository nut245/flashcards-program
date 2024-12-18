import json
import collections.abc

def update_json_file(file, updated_value: dict, append=False):
    """
    changes the values within json file

    ### Parameters
    - updated_value: dict
        - a smaller dictionary than the json file, 
        ideally sharing select keys with different values

    a static function, usable within all files/classes, but particularly SettingsPage()
    """
    write_to_json_file(
        file=file,
        data=update_json(
            dictionary=parse_json(file=file), 
            updated_value=updated_value,
            append=append
        )
    )

def parse_json(file):
    """
    to open and later insert values of json file

    ### Returns
    - config: dict
        - json file as dictionary in python
    """
    with open(file, 'r') as jsonFile:
        data = jsonFile.read()
    config: dict = json.loads(data)
    return config

def write_to_json_file(file, data: dict):
    """
    updates and rewrites information within settings_config.json file with conventional formatting
    """
    with open(file, 'w') as jsonFile:
        json.dump(data, jsonFile, indent=4)

def update_json(dictionary: dict, updated_value: dict, append=False):
    """
    navigates settings_config dictionary and compares values within another dictionary

    replaces/updates values under congruent dictionary keys

    ### Parameters
    - dictionary: dict
        - the settings_config.json file converted into python dictionary
    - updated_value: dict
        - another dictionary, ideally sharing select keys with different values

    ### Returns
    - modified dictionary parameter

    ### Raises
    - MyOwnError: Exception | str
        - outputs incongruous keys within updated_value dict
    """
    for key, value in updated_value.items():
        if isinstance(value, collections.abc.Mapping):
            dictionary[key] = update_json(dictionary.get(key, {}), value, append=append)
        elif key in dictionary:
            if value == None:
                value = {}
            dictionary[key] = value
        else:
            if append:
                dictionary[key] = value
            else:
                print(f"{__name__} file. (MyOwnError): the key and/or path to, '{key}', does not exist in data file\n")
    return dictionary