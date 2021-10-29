from bs4 import BeautifulSoup
import requests
import json

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

html = requests.get('https://www.google.com/search?q=potato&oq=potato',
                    headers=headers).text

soup = BeautifulSoup(html, 'lxml')

summary = []

for container in soup.findAll('div', class_='tF2Cxc'):
    heading = container.find('h3', class_='LC20lb DKV0Md').text
    link = container.find('a')['href']

    summary.append({
        'Heading': heading,
        'Link': link,
    })

print(json.dumps(summary, indent=2, ensure_ascii=False))