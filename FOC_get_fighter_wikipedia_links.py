import json
from urllib.request import urlopen

url = r"""https://en.wikipedia.org/w/api.php?action=query&prop=links&pllimit=499&"""
url += r"""titles=List_of_male_mixed_martial_artists&format=json"""
page = urlopen(url)
full_html = page.read().decode("utf-8")
a_dict = json.loads(full_html)
pl_continue_var = a_dict["continue"]["plcontinue"]
print("Value of plcontinue: %s" % pl_continue_var)
while 1 > 0:
    url = r"""https://en.wikipedia.org/w/api.php?action=query&plcontinue=%s""" % pl_continue_var
    url += """&prop=links&pllimit=499&titles=List_of_male_mixed_martial_artists&format=json"""
    page = urlopen(url)
    html = page.read().decode("utf-8")
    full_html += html
    a_dict = json.loads(html)
    if "batchcomplete" in a_dict:
        break
    pl_continue_var = a_dict["continue"]["plcontinue"]
    print("Value of plcontinue: %s" % pl_continue_var)
only_links = full_html[full_html.find('"links"'):full_html.find('"ns":1')]
fighter_links_unfiltered = only_links.split("},{")
fighter_links_unfiltered = [element[15:] for element in fighter_links_unfiltered]
fighter_links_unfiltered = [element[1:-1] for element in fighter_links_unfiltered]
with open("FOC_countries.txt", "r") as handle:
    countries = handle.readlines()
    countries = [element[3:-1] for element in countries]
fighter_links = [element for element in fighter_links_unfiltered if element not in countries and
                 (element.find("Championship") == -1 or
                 element.find("championship") == -1)]
with open("FOC_fighter_wikipedia_links.txt", "w") as handle:
    for element in fighter_links:
        handle.write(element + "\n")
