from datetime import datetime
import re

import requests
from bs4 import BeautifulSoup

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
                return lat.strip(), lon.strip()
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

        capcodes = list(set(capcodes))
        return capcodes

    def to_datetime(date_str):
        """Converts a date string to SQL Server datetime format."""
        # Assuming format is "HH:MM:SS DD-MM-YY"
        dt = datetime.strptime(date_str, "%H:%M:%S %d-%m-%y")

        # SQL Server datetime format: 'YYYY-MM-DD HH:MM:SS'
        return dt.strftime("%Y-%m-%d %H:%M:%S")

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

            coords = parse_coords(cells[2])
            if coords:
                lat, lon = coords
            else:
                lat, lon = None, None

            message_data.append({
                "timestamp": to_datetime(cells[0].text.strip()),
                "type": cells[1].text.strip(),
                "message": cells[2].text,
                "capcodes": parse_capcodes(index),
                "coords": (lat, lon) if lat and lon else None,
                "vehicles": parse_vehicle(cells[2]),
            })
    return message_data
