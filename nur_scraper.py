import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd

nur_url = "https://www.nur.kz"
nur_response = requests.get(nur_url)
nur_soup = BeautifulSoup(nur_response.content, "html.parser")

nur_headlines = nur_soup.select(".article-card")
data = {
    'org': nur_url,
    'scraped_at': datetime.datetime.now(),
    'headline_1': '',
    'headline_2': '',
    'headline_3': '',
}
headlines=[]
links = []
for idx, h in enumerate(nur_headlines[:4]):
    try:
        headline = (h.select('h3.article-card__title')[0].text.replace(u'\xad', ''))
        headlines.append(headline)
        links.append(h.find('a', href=True))
    except:
        pass

def dups(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

nHeadlines = dups(headlines)
nLinks = dups(links)
for i in range(0, len(nHeadlines)):
    key = f'headline_{i+1}'
    value = str(nHeadlines[i]) + ", " + nur_url + str(nLinks[i]['href'])
    data[key] = value

df = pd.DataFrame(data, index=[0])

try:
    existing_df = pd.read_csv("updated_headlines.csv")
except:
    existing_df = pd.DataFrame([])

combined = pd.concat([df, existing_df], ignore_index=True)

combined.to_csv("updated_headlines.csv", index = False)
