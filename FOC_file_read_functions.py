from urllib.request import urlopen
import urllib.parse
import json


# Given a list of data from fighter data file, return the names and the url translated names
def get_names_and_urls():
    with open("FOC_collect_stats/FOC_basic_fighter_stats.json", "r", encoding='utf-8') as handle:
        some_data = json.load(handle, strict=False)
    some_data = some_data['data']
    fighter_key_string_list = [str(fighter.keys()) for fighter in some_data]
    fighter_names = [fighter[fighter.find("[") + 2:fighter.rfind("]") - 1] for fighter in fighter_key_string_list]
    names = sorted(fighter_names)
    urls = [fighter.replace(" ", "_") for fighter in fighter_names]
    urls = [urllib.parse.quote(fighter) for fighter in urls]
    return names, urls


def remove_paren(a_string):
    """Remove parenthesis from a string"""
    if a_string.find("(") > 0:
        index = a_string.find("(")
        return a_string[:index-1]
    else:
        return a_string