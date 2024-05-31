import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://tengrinews.kz/"
response = requests.get(url)
te_soup = BeautifulSoup(response.content, 'html.parser')

te_headlines = te_soup.find('section', {'id': 'new-relic-top-stories'})
te_h3 = te_headlines.find_all('h3')

data = {
    'org': url,
    'scraped_at': datetime.datetime.now(),
    'headline_1': '',
    'headline_2': '',
    'headline_3': '',
}

headlines = []
links = []
for idx, h in enumerate(te_h3[:3]):
    try:
        headlines.append(h.text)
        links.append(h.find('a', href=True))
    except: 
        pass

for i in range(0, len(headlines)):
    key = f'headline_{i+1}'
    value = str(headlines[i]) + ", " + url + str(links[i]['href'])
    data[key] = value

df = pd.DataFrame(data, index= [0])
print(df.head())

try:
    existing_df = pd.read_csv("updated_headlines.csv")
except:
    existing_df = pd.DataFrame([])

combined = pd.concat([df, existing_df], ignore_index=True)

combined.to_csv("updated_headlines.csv", index=False)
