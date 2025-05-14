import requests
from bs4 import BeautifulSoup

URL = "https://www.p2000-online.net/p2000.py?aantal=30&kennemerland=1&pagina=0"

response = requests.get(URL)
response.encoding = "UTF-8"
soup = BeautifulSoup(response.text, "html.parser")

rows = soup.find_all("tr")
berichten = []

i = 0
while i < len(rows):
    cells = rows[i].find_all("td")
    if len(cells) == 4 and "DT" in cells[0].get("class", []):
        bericht = {
            "datetime": cells[0].text.strip(),
            "type": cells[1].text.strip(),
            "region": cells[2].text.strip(),
            "message": cells[3].text.strip()
        }
        berichten.append(bericht)
    i += 1

for bericht in berichten:
    print(f"{bericht['datetime']} - {bericht['type']} - {bericht['region']}")
    print(f"  Message: {bericht['message']}")
    print("-" * 80)
