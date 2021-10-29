from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote, unquote
import time
from FOC_Fight import Fight
from FOC_Fighter import Fighter
from FOC_get_detailed_fighter_stats import read_detailed_stats_from_file
from FOC_file_read_functions import get_names_and_urls, remove_paren
import ssl
from urllib.error import HTTPError

#https://stackoverflow.com/questions/51390968/python-ssl-certificate-verify-error
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
"""This import statement is from 
https://stackoverflow.com/questions/8234274/how-to-indent-the-contents-of-a-multi-line-string"""
try:
    import textwrap
    textwrap.indent
except AttributeError:  # undefined function (wasn't added until Python 3.3)
    def indent(text, amount, ch=' '):
        padding = amount * ch
        return ''.join(padding+line for line in text.splitlines(True))
else:
    def indent(text, amount, ch=' '):
        return textwrap.indent(text, amount * ch)


def parse_division(a_string):
    """Return formatted fighter division"""
    if a_string == "UNKNOWN_DIVISION":
        return a_string
    parsed_divisions = []
    for element in a_string.split():
        if element.find("weight") > 0:
            parsed_divisions.append(element)
    a_list = [element.lower() for element in parsed_divisions]
    a_set = set(a_list)
    a_list = [element.capitalize() for element in list(a_set)]
    return a_list


def parse_weight(a_string):
    """Return formatted fighter weight"""
    if a_string == "UNKNOWN_WEIGHT":
        return a_string
    a_string = remove_paren(a_string)
    if a_string.find("\\") > 0:
        a_string = a_string[:a_string.find("\\")]
    if a_string.lower().find("lb") > 0:
        return a_string
    elif a_string.lower().find("kg") > 0:
        parsed = a_string[:a_string.lower().find("kg")-1]
        a_float = float(parsed)*2.20462
        a_string = str(round(a_float, 1))
        return a_string + " lb"
    else:
        return "UNKNOWN_WEIGHT"


def find_mma_section(some_html):
    """If a fighter's wikipedia article includes many sections, call this to find the mma section"""
    index = some_html.find('id="Mixed_martial_arts_record"')
    if index == -1:
        return some_html
    else:
        return some_html[index:]


def find_weight(a_soup):
    """Find a fighter's weight from their Wikipedia page"""
    tables = a_soup.find_all("table")
    table = None
    for a_table in tables:
        if (a_table['class'] == ['infobox', 'vcard'] or a_table['class'] == ['infobox', 'biography', 'vcard'])\
                and (str(a_table).find("Weight") > 0 or str(a_table).find("Billed weight") > 0):
            table = a_table
            break
        else:
            return "UNKNOWN_WEIGHT"
    if table is None:
        return "UNKNOWN_WEIGHT"
    a_list = table.find_all("tr")
    selected_row = ""
    try:
        for element in a_list:
            header = element.find("th")
            if str(header).find("Weight") != -1 or str(header).find("Billed weight") != -1:
                selected_row = element
                break
    except (AttributeError, UnboundLocalError):
        print("ERROR: weight not found")
        return "UNKNOWN_WEIGHT"
    if selected_row == "":
        return "UNKNOWN_WEIGHT"
    tag = selected_row.find("td")
    if not tag.string:
        selected_row_string = str(selected_row)
        a_substring = selected_row_string[selected_row_string.find("infobox-data"):]
        the_weight = a_substring[a_substring.find(">")+1:a_substring.find("<")]
        return str(the_weight)
    else:
        return str(tag.string)


def find_division(a_soup):
    """Find a fighter's division from their Wikipedia page"""
    tables = a_soup.find_all("table")
    table = None
    for a_table in tables:
        if (a_table['class'] == ['infobox', 'vcard'] or a_table['class'] == ['infobox', 'biography', 'vcard']) \
                and ((str(a_table).find("Division") > 0) or str(a_table).find("Weight") > 0):
            # print(str(a_table.prettify()))
            table = a_table
            break
        else:
            return "UNKNOWN_DIV"
    if not table:
        return "UNKNOWN_DIV"
    a_list = table.find_all("tr")
    selected_row = ""
    try:
        for element in a_list:
            header = element.find("th")
            if str(header).find("Division") != -1:
                selected_row = element
                break
    except (AttributeError, UnboundLocalError):
        print("ERROR: division not found")
        return "UNKNOWN_DIV"
    if selected_row == "":
        return "UNKNOWN_DIV"
    tag = selected_row.find("td")
    anchors = tag.find_all("a")
    if not anchors:
        return tag.string
    divisions = []
    division_string = ""
    for element in anchors:
        if element.has_attr("title"):
            divisions.append(element['title'])
            division_string += str(element['title'])
            division_string += " * "
    return division_string


def find_fights(a_soup, name):
    """Find a fighter's fights from their Wikipedia page"""
    tables = a_soup.find_all("table")
    table = None
    for a_table in tables:
        body = a_table.find("tbody")
        if a_table.has_attr("class") and (a_table['class'] == ['wikitable'] or a_table['class'] == ['wikitable', 'sortable']) and str(body).find("Opponent") > 0 and str(body).find("Record") > 0:
            table = a_table
            break
    if table is None:
        return []
    rows = table.find_all("tr")
    a_data = rows[0].find("td")
    if not a_data:
        rows = rows[1:]
    elif a_data.has_attr("style"):
        pass
    # Need to fix, Dewey Cooper, weird style in html ^
    else:
        rows = rows[1:]
        # print("NO")
    fights = []
    saved_date = ""
    repeat = 1
    for row in rows:
        all_data = row.find_all("td")
        if not all_data or len(all_data) < 8:
            return []
        result = all_data[0].get_text()[:-1]
        fighterB = all_data[2].get_text()[:-1].replace('"',"'")
        method = all_data[3].get_text()[:-1]
        if repeat == 1:
            date = all_data[5].get_text()[:-1]
            round = all_data[6].string[:-1]
            time = all_data[7].get_text()[:-1]
            if time == "N\\A":
                time = "Not applicable"
            a_fight = Fight(name, fighterB, result, method, date, round, time)
            # a_fight.print_stats()
            fights.append(a_fight)
        else:
            date = saved_date
            round = all_data[4].string[:-1]
            # print(round)
            time = all_data[5].get_text()[:-1]
            if time == "N\\A":
                time = "Not applicable"
            # print(time)
            repeat = repeat-1
            # print("REPEAT IS NOW: " + str(repeat))
            a_fight = Fight(name, fighterB, result, method, date, round, time)
            #a_fight.print_stats()
            fights.append(a_fight)
        if all_data[5].has_attr("rowspan"):
            saved_date = all_data[5].find("span").string
            repeat = int(all_data[5]['rowspan'])
            # print("REPEAT: " + str(repeat))
    if type(fights) == str:
        return Fight("UNKNOWN_FIGHTS", "", "", "", "", "")
    return fights


def get_fighter_json(a_fighter):
    """Given a Fighter object, return the json string representing it"""
    a_str = indent('{\n"%s":\n\t{\n\t\t"stats":\n' % a_fighter.name, 4)
    a_str += indent(a_fighter.get_json(), 12)
    a_str += indent(',\n\t\t"fights":[\n', 4)
    for i, a_fight in enumerate(a_fighter.fights):
        if i == len(a_fighter.fights) - 1:
            a_str += indent(a_fight.get_json(), 12) + "\n"
        else:
            a_str += indent(a_fight.get_json(), 12) + ",\n"
    a_str += indent('\t\t]\n\t}\n}', 4)
    return a_str


def main():
    start_time = time.time()
    with open("../FOC_fighter_wikipedia_links_edited.txt", "r", encoding="utf-8") as handle:
        data = handle.readlines()
    names = [fighter[:-1] for fighter in data]
    urls = [quote(a_fighter.replace(" ", "_").encode('utf-8')) for a_fighter in names]
    the_fighters = []
    i = 0
    detailed_stats_dict = read_detailed_stats_from_file("FOC_detailed_fighter_stats.json")
    with open("FOC_basic_fighter_stats.json", "w", encoding="utf-8") as handle:
        handle.write('{"data":[\n')
        list_len = len(urls)
        while i < list_len:
            url = "https://en.wikipedia.org/wiki/%s" % urls[i]
            print("\nThe Wikipedia URL: %s" % url)
            have_HTTP_error = False
            try:
                page = urlopen(url)
            except HTTPError:
                have_HTTP_error = True
                print("Couldn't find page for " + names[i])
                f = open("FOC_unknown_wiki_pages.txt", "w", encoding='utf-8')
                f.write(names[i] + "\n")
                f.close()
            if have_HTTP_error == False:
                html = page.read().decode("utf-8")
                soup = BeautifulSoup(html, "html.parser")
                fights_soup = BeautifulSoup(find_mma_section(html), "html.parser")
                weight = find_weight(soup)
                weight = parse_weight(weight)
                # assert(type(weight) == str)
                division = find_division(soup)
                division = parse_division(division)
                fights = find_fights(fights_soup, names[i])
                assert (type(fights) == list)
                for a_fight in fights:
                    assert (type(a_fight) == Fight)
                some_fighter = Fighter(names[i], weight, division, fights, detailed_stats_dict[names[i]])
                assert (type(some_fighter) == Fighter)
                the_fighters.append(some_fighter)
                handle.write(get_fighter_json(some_fighter))
                if i != list_len - 1:
                    handle.write(",\n")
                else:
                    handle.write("\n")
                some_fighter.print_stats()
                if detailed_stats_dict[names[i]] != {}:
                    some_fighter.print_detailed_stats()
                some_fighter.print_fights()
            i += 1
        handle.write("\t]\t\n}")
    rounded_time = round(time.time() - start_time, 3)
    print("--- %s second runtime to find all stats ---" % rounded_time)


if __name__ == "__main__":
    main()




