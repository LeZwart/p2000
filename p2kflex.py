import requests
from bs4 import BeautifulSoup
import re

url = "https://monitor.p2kflex.nl/hdb/engine.php"
headers = {
    "Referer": "https://monitor.p2kflex.nl/hdb/"
}


def scrape_region(region, limit=50):
    def parse_coords(message_cell):
        """Parses coordinates from messages,
            not all messages contain coordinates.
        Args:
            message_cell (bs4.element.Tag): Contains message including coords,
                vehicle info, etc.
        Returns:
            dict: A dictionary with latitude and longitude
                if coordinates are found, otherwise None.
            If the message does not contain coordinates, returns None.
        Raises:
            None: If the message does not contain coordinates.
        """

        link = message_cell.find("a", href=True)
        if link and "ShowMap" in link["href"]:
            match = re.search(r"ShowMap\('([\d\.,-]+)'\)", link["href"])
            if match:
                coords = match.group(1)
                lat, lon = coords.split(",")
                return {"lat": float(lat), "lon": float(lon)}
        return None

    def parse_vehicle(message_cell):
        vehicles = []

        spans = message_cell.find_all("span", id="BB")
        vehicles.extend(span.text.strip() for span in spans)

        return vehicles

    def parse_capcodes(index):
        capcodes = []
        for row in rows[index + 1:]:
            children = list(row.children)
            if len(children) > 1 and "capcode" in children[1].get("class", []):
                capcodes.append(children[1].text.strip())
            else:
                break
        return capcodes

    # Example timestamp 13:05:51 03-06-25
    def convert_timestamp(timestamp):
        """Converts timestamp to unix timestamp."""

        match = re.match(
            r"(\d{2}:\d{2}:\d{2}) (\d{2})-(\d{2})-(\d{2})", timestamp)

        if match:
            time_str, day, month, year = match.groups()
            year = int(year) + 2000  # Assuming year is in 2000s
            return f"{year}-{month}-{day} {time_str}"
        return timestamp
    
    params = {
        "id": "0",
        "regio": region,
        "limit": limit,
    }

    response = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr")

    message_data = []
    first_message = True
    for index, row in enumerate(rows):
        cells = row.find_all("td")
        if "datetime" in cells[0].get("class", []):
            # First message is always malformed, skip it
            if first_message:
                first_message = False
                continue

            message_data.append({
                "timestamp": cells[0].text.strip(),
                "type": cells[1].text.strip(),
                "message": cells[2].text,
                "capcodes": parse_capcodes(index),
                "coords": parse_coords(cells[2]),
                "vehicles": parse_vehicle(cells[2]),
            })
    return message_data
