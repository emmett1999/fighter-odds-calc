import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import urllib.error
from urllib.parse import quote

"""Writes the names of fighters with valid wikipedia pages to a file"""
def main():
    # https://stackoverflow.com/questions/51390968/python-ssl-certificate-verify-error
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

    with open("FOC_potential_fighters.json", "r", encoding='utf-8') as fh:
        data = json.load(fh)
    key_list = data.keys()
    url_parsed_name_list = [quote(a_key.strip().replace(" ", "_").encode('utf-8')) for a_key in key_list]
    url_list = ["https://en.wikipedia.org/wiki/" + a_name for a_name in url_parsed_name_list]
    with open("FOC_potential_valid_fighters.txt", "w", encoding="utf-8") as fh:
        for u in url_list:
            print(u)
            has_error = False
            try:
                page = urlopen(u)
            except urllib.error.HTTPError:
                has_error = True
            if has_error == False:
                parsed = u[u.rfind("/")+1:]
                parsed_again = parsed.replace("_"," ")
                print(parsed_again)
                fh.write(parsed_again + "\n")


if __name__ == "__main__":
    pass
    #main()
