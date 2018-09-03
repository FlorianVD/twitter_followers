import json
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

with open('sofie_be.json', 'r') as input:
    companies = json.load(input)

output = {}
output["Bedrijven"] = []

for company in companies["Bedrijven"]:
    website = company["url"]

    print(website)

    request = Request(website)
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
    
    try:
        response = urlopen(request).read()
    except:
        name = company["name"]
        output["Bedrijven"].append({
            "name": name,
            "url" : website
        })
        continue

    soup = BeautifulSoup(response,'html.parser')

    name = ""
    for tag in soup.find_all('meta'):
        if(tag.get('property', None) == "author"):
            name = tag.get('content', None)
        if(tag.get('property', None) == "og:site_name"):
            name = tag.get('content', None)

    output["Bedrijven"].append({
        "name": name if name else company["name"],
        "url" : website
    })

with open('dashplus_belgium.json', 'w') as file:
    json.dump(output, file)
print('Done')