# This small project scrapes data from the first two pages of the hackernews website.


import requests
from bs4 import BeautifulSoup
import pprint


#beautiful soup allows to use HTML and grab different data
#request module allows us to download the HTML

res=requests.get('https://news.ycombinator.com/news')
#scraping page 2
res2 = requests.get('https://news.ycombinator.com/news?p=2')

#Modify data into useable HTML

soup= BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')
links = soup.select('.titleline')
subtext = soup.select('.subtext')
links2 = soup2.select('.titleline')
subtext2 = soup2.select('.subtext')

all_links = links + links2
all_subtext = subtext + subtext2

def create_custom_hn(links, votes):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.find('a').get('href')
        vote = votes[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace('points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return hn

pprint.pprint(create_custom_hn(all_links, all_subtext))

