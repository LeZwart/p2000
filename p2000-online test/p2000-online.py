import requests
from bs4 import BeautifulSoup
import json

berichten = []
for pagina in range(0, 1001):
    URL = (
        f"https://www.p2000-online.net/p2000.py?aantal=30"
        f"&kennemerland=1&pagina={pagina}"
    )

    response = requests.get(URL)
    response.encoding = "UTF-8"
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.find_all("tr")

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
        break
    print(f"Page {pagina}/1000 processed.")

with open("berichten.json", "a") as f:
    json.dump(berichten, f, ensure_ascii=False, indent=4)
