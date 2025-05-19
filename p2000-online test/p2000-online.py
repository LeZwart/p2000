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

    for index, row in enumerate(rows):
        cells = row.find_all("td")
        if len(cells) == 4 and "DT" in cells[0].get("class", []):

            # FIXME: Duplicates capcodes somehow
            capcodes = []
            for next_row in rows[index + 1:]:
                td = next_row.find("td", class_="OmsAm")
                if td:
                    raw_capcode = td.text.strip()

                    capcode = raw_capcode.split()[0]
                    if len(capcode) == 6:
                        capcode = "0" + capcode
                    elif len(capcode) == 7:
                        capcode = capcode
                    else:
                        continue
                    capcodes.append(capcode)
                elif not next_row.find_all("td"):
                    continue
                else:
                    break

            bericht = {
                "datetime": cells[0].text.strip(),
                "type": cells[1].text.strip(),
                "region": cells[2].text.strip(),
                "message": cells[3].text.strip()
            }
            berichten.append(bericht)

    print(f"Page {pagina}/1000 processed.")

with open("berichten.json", "w", encoding="utf-8") as f:
    json.dump(berichten, f, ensure_ascii=False, indent=4)
