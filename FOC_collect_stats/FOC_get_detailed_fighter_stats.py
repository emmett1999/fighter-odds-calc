from FOC_file_read_functions import get_names_and_urls
import requests
from bs4 import BeautifulSoup
import json
from urllib.request import urlopen
import time


def get_google_link_results(query):
    headers = {
        'User-agent':
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    url_string = 'https://www.google.com/search?q=' + query + '&oq=' + query
    html = requests.get(url_string, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    some_links = []
    for container in soup.findAll('div', class_='tF2Cxc'):
        heading = container.find('h3', class_='LC20lb DKV0Md').text
        link = container.find('a')['href']
        some_links.append(link)
    return some_links


def parse_links(some_links):
    for l in some_links:
        if l.find('ufcstats.com/fighter-details/') > 0:
            return l
    return ""


def find_detailed_stats(a_link, fighter_name):
    #write tests for making sure the stat name = dictionary name (not wrong position or data)
    if a_link == '':
        return {fighter_name:{}}
    try:
        page = urlopen(a_link)
    except (TimeoutError, EOFError) as e:
        return {fighter_name:{}}
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    stat_class = soup.find('div', class_='b-list__info-box-left clearfix')
    all_stats = stat_class.findAll('li', class_='b-list__box-list-item b-list__box-list-item_type_block')
    stat_dict = {}
    stat_names = ['SLpM','StrAcc','SApM','StrDef','TDAvg','TDAcc','TDDef','SubAvg']
    #print("SIZE!: " + str(len(all_stats)))
    filtered_containers = [stat for stat in all_stats if stat.text.strip()[stat.find(':'):] != '']
    for i, a in enumerate(filtered_containers):
        stat_text = a.text.strip()
        stat_name = stat_text[:stat_text.find(':'):]
        stat_number = stat_text[stat_text.rfind(" ")+1:]
        stat_dict[stat_names[i]] = stat_number
    real_dict = {fighter_name:stat_dict}
    return real_dict


def dict_to_json(a_dict):
    return json.dumps(a_dict, indent= 4)


def main():
    start_time = time.time()
    with open("../FOC_fighter_wikipedia_links_edited.txt", "r", encoding="utf-8") as handle:
        data = handle.readlines()
    names = [f[:-1] for f in data]
    i = 0
    with open("FOC_detailed_fighter_stats.json", "w", encoding='utf-8') as fh:
        fh.write('{"detailedStats":[\n')
        while i < len(names):
            print(names[i])
            the_query = 'ufc stats ' + names[i]
            links = get_google_link_results(the_query)
            the_link = parse_links(links)
            print("The link: " + the_link)
            if the_link == "":
                detailed_stats_dict = {names[i]:{}}
            else:
                detailed_stats_dict = find_detailed_stats(the_link, names[i])
            print(dict_to_json(detailed_stats_dict))
            fh.write(dict_to_json(detailed_stats_dict))
            if i != len(names)-1:
                fh.write(",\n")
            else:
                fh.write("\n")
            i = i+1
        fh.write("\t]\n}")
    rounded_time = round(time.time() - start_time, 3)
    print(rounded_time)


def read_detailed_stats_from_file(filename):
    """Given a json file, read it and return a dictionary"""
    with open(filename, "r", encoding='utf-8') as fh:
        a_dict = json.load(fh)
    fighter_list = a_dict['detailedStats']
    for a_fighter in fighter_list:
        fighter_name = list(a_fighter.keys())[0]
        a_dict[fighter_name] = a_fighter[fighter_name]
    return a_dict


if __name__ == "__main__":
    pass
    #main()
