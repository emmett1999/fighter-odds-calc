from FOC_file_read_functions import get_names_and_urls
import requests
from bs4 import BeautifulSoup
import json
from urllib.request import urlopen
import time
from PIL import Image
from io import BytesIO
import ssl
from urllib3.exceptions import InsecureRequestWarning

def read_fighter_image_links_from_file(filename):
    with open(filename, "r", encoding="utf-8") as fh:
        a_dict = json.load(fh)
    return a_dict

def find_fighter_image_url(url):
    """The url parameter is the page that is being searched. The link to the fighter's image is returned"""
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    html = requests.get(url, verify=False).text
    soup = BeautifulSoup(html, "html.parser")
    the_image_link = soup.find("meta", property="og:image")
    if not the_image_link:
        return ""
    return the_image_link["content"]


def main():
    start_time = time.time()

    with open("FOC_fighter_wikipedia_links_edited.txt", "r", encoding="utf-8") as handle:
        data = handle.readlines()
    a_tuple = get_names_and_urls()
    names = a_tuple[0]
    urls = a_tuple[1]

    fighter_image_dict = {}
    i = 0
    while i < len(names):
        print("Name: " + names[i] + " Url name: " + urls[i])
        full_url = "https://en.wikipedia.org/wiki/" + urls[i]
        print("Actual url: " + full_url)
        image_url = find_fighter_image_url(full_url)
        print("Image url: " + image_url)
        fighter_image_dict[names[i]] = image_url
        i = i+1
    json_object = json.dumps(fighter_image_dict, indent=4)
    with open("FOC_fighter_image_links.json", "w", encoding="utf-8") as fh:
        fh.write(json_object)
    rounded_time = round(time.time() - start_time, 3)
    print("--- %s second runtime ---" % rounded_time)


if __name__ == "__main__":
    main()