from urllib.parse import unquote
from urllib.parse import quote
import ssl
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.parse
import json
import time


def write_list_to_file(filename, list_name):
    with open(filename, "w", encoding="utf-8") as fh:
        for n in list_name:
            fh.write(n + '\n')


def add_all_potential_fighters():
    with open("../FOC_fighter_wikipedia_links_edited.txt", "r", encoding="utf-8") as fh:
        data = fh.readlines()
    data[-1] + '\n'
    existing_fighters = [name[:-1] for name in data]
    #print(existing_fighters)
    with open("FOC_potential_valid_fighters.txt", "r", encoding="utf-8") as fh:
        data = fh.readlines()
    potential_valid = [unquote(name[:-1]) for name in data]
    existing_fighters.extend(potential_valid)
    no_dup = sorted(list(dict.fromkeys(existing_fighters)))
    print(len(no_dup))
    write_list_to_file("../FOC_fighter_wikipedia_links_edited.txt", no_dup)


def main():
    start_time = time.time()
    # https://stackoverflow.com/questions/51390968/python-ssl-certificate-verify-error
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context
    with open("../FOC_fighter_wikipedia_links_edited.txt", "r", encoding="utf-8") as fh:
        data = fh.readlines()
    name_list = [f[:-1] for f in data]
    useful_name_dict = {}
    url_parsed_name_list = [quote(a_fighter.replace(" ", "_").encode('utf-8')) for a_fighter in name_list]
    with open("../FOC_fighter_wikipedia_links_edited.txt", "w", encoding="utf-8") as fh:
        for i, u in enumerate(url_parsed_name_list):
            a_url = "http://en.wikipedia.org/wiki/" + u
            a_name = name_list[i]
            useful = is_wikipedia_page_useful(a_url)
            has_other_url = False
            if not useful:
                other_url = a_url + "_(mixed_martial_artist)"
                has_other_url = True
                success = test_open(other_url)
                if success:
                    useful = True
            if useful and has_other_url:
                useful_name_dict[a_name] = other_url
                new_name = a_name + " (mixed martial artist)"
                fh.write(new_name + '\n')
            elif useful:
                useful_name_dict[a_name] = a_url
                fh.write(a_name + '\n')
            if useful:
                name_list.append(a_name)
                print("Name: " + a_name + " url: " + useful_name_dict[a_name])
            else:
                print(a_name + " not useful")
    with open("FOC_fighter_url_dict.json", "w", encoding='utf-8') as fh:
        fh.write(json.dumps(useful_name_dict, indent=4))
    rounded_time = round(time.time() - start_time, 3)
    print("--- %s second runtime to find all stats ---" % rounded_time)


def test_open(url):
    try:
        page = urlopen(url)
    except urllib.error.HTTPError:
        return False
    return True


def is_wikipedia_page_useful(fighter_url):
    """Access the fighter wikipedia page and determine if they should be in the database"""
    have_http_error = False
    try:
        page = urlopen(fighter_url)
    except urllib.error.HTTPError:
        return False
    if not have_http_error:
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        paras = soup.findAll("p")
        parasTest = soup.findAll("p", {"class": "mw-empty-elt"})
        valid_paras = [i for i in paras if i not in parasTest]
        para = valid_paras[0]
        if not para.b:
            return False
        else:
            if para.text.find("martial") >= 0 or para.text.find("MMA") >= 0:
                return True
    return False


if __name__ == "__main__":
    #add_all_potential_fighters()
    main()
