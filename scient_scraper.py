import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd

sc_url = "https://scientificrussia.ru/"
sc_response = requests.get(sc_url)
sc_soup = BeautifulSoup(sc_response.content, 'html.parser')

sc_headlines = sc_soup.select('h2', attrs={'data-testid': 'card-headline'})
sc_links = sc_soup.find('div', attrs = {'data-testid': 'vermont-section'})
sc_a = sc_links.find_all('a')
#print(bbc_a)

data = {
    'org': sc_url,
    'scraped_at': datetime.datetime.now(),
    'headline_1': '',
    'headline_2': '',
    'headline_3': '',
}

headlines = []
# Skip first two main headlines in BBC 
for idx, h in enumerate(sc_headlines[2:5]):
    try:
        headlines.append(h.text)
    except: 
        pass

links = []
for idx, a in enumerate(sc_a[2:5]):
    try: 
        link = a['href']  
        if(link.startswith(sc_url)):
            links.append(link)
        else:
            links.append(sc_url+link)
    except:
        pass

for i in range(0, len(headlines)):
    key = f'headline_{i+1}'
    value = str(headlines[i]) + ', ' + str(links[i])
    data[key] = value

df = pd.DataFrame(data, index= [0])
try:
    existing_df = pd.read_csv("updated_headlines.csv")
except:
    existing_df = pd.DataFrame([])

combined = pd.concat([df, existing_df], ignore_index=True)

combined.to_csv("updated_headlines.csv", index=False)
