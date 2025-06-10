import SQLServer
from p2kflex import scrape_region

REGION_COUNT = 25
LIMIT = 30000


def main():
    conn = SQLServer.connect("P2000")
    cursor = conn.cursor()

    all_messages = []
    for i in range(1, REGION_COUNT + 1):
        region = f"R{i}"

        region_data = scrape_region(region, LIMIT)
        all_messages.extend(region_data)
        print(f"Scraped data for {region}: {len(region_data)} records")
    print(f"Total records scraped: {len(all_messages)}")

    for message in all_messages:
        save_message_to_db(message, cursor)
    conn.commit()


def save_message_to_db(message, cursor):
    """Saves a single message to the database."""

    STMT = (
        "INSERT INTO Bericht (datum, beschrijving, lat, lon) "
        "VALUES (?, ?, ?, ?)"
    )

    lat, lon = None, None
    if "coords" in message and message["coords"] is not None:
        lat, lon = message["coords"]

    cursor.execute(STMT, (
        message["timestamp"],
        message["message"],
        lat,
        lon
    ))

    # Retrieve the last inserted bericht_id
    cursor.execute("SELECT MAX(id) FROM Bericht")
    bericht_id = cursor.fetchone()[0]

    if bericht_id is None:
        bericht_id = 1

    # Insert relation to capcodes
    for capcode in message["capcodes"]:
        capcode_id = SQLServer.get_capcode_id(cursor, capcode)
        if capcode_id is None:
            cursor.execute(
                "INSERT INTO Capcode (capcode) VALUES (?)",
                (capcode,)
            )
            capcode_id = SQLServer.get_capcode_id(cursor, capcode)

        cursor.execute(
            "INSERT INTO BerichtCapcode (bericht_id, capcode_id) "
            "VALUES (?, ?)",
            (bericht_id, capcode_id)
        )

    return


if __name__ == "__main__":
    main()
