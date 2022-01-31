import urllib.parse
import json


def get_names_and_urls(filename):
    """Given a list of data from fighter data file, return the names and the url translated names"""
    with open(filename, "r", encoding='utf-8') as handle:
        some_data = json.load(handle, strict=False)
    data = some_data['data']
    fighter_key_string_list = [str(fighter.keys()) for fighter in data]
    fighter_names = [fighter[fighter.find("[") + 2:fighter.rfind("]") - 1] for fighter in fighter_key_string_list]
    sorted_names = sorted(fighter_names)
    urls = [fighter.replace(" ", "_") for fighter in fighter_names]
    parsed_urls = [urllib.parse.quote(fighter) for fighter in urls]
    return sorted_names, parsed_urls


def determine_weightclass(weight_num):
    if weight_num < 135:
        return "Flyweight"
    elif 135 <= weight_num < 145:
        return "Bantamweight"
    elif 145 <= weight_num < 155:
        return "Featherweight"
    elif 155 <= weight_num < 170:
        return "Lightweight"
    elif 170 <= weight_num < 185:
        return "Welterweight"
    elif 185 <= weight_num < 205:
        return "Middleweight"
    elif 205 <= weight_num <= 210:
        return "Light heavyweight"
    elif weight_num > 210:
        return "Heavyweight"
    else:
        return "UNKNOWN_WEIGHT"


def remove_paren(a_string):
    """Remove parenthesis from a string"""
    if a_string.find("(") > 0:
        index = a_string.find("(")
        return a_string[:index-1]
    else:
        return a_string


def read_glicko_ranking(filename):
    with open(filename, "r", encoding="utf-8") as fh:
        data = fh.readlines()
    a_glicko_dict = {}
    for line in data:
        the_glicko = line[line.rfind("2:") + 3:-1]
        fighter_name = line[9:line.find("Glicko")]
        fighter_name = fighter_name.rstrip()
        a_glicko_dict[fighter_name] = float(the_glicko)
    return a_glicko_dict


def convert_dict_keys_fighter(a_fighter_object_dict):
    fighter_list_keys = list(a_fighter_object_dict)
    for key in fighter_list_keys:
        if key.find("(") > 0:
            parsed_key = key[:key.find("(") - 1]
            a_fighter_object_dict[parsed_key] = a_fighter_object_dict[key]
            a_fighter_object_dict[parsed_key].name = parsed_key
            del a_fighter_object_dict[key]
    return a_fighter_object_dict
