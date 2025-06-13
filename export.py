import pandas as pd
import SQLServer


def export_to_csv(cursor, filename):
    """Exports the Bericht table to a CSV file to later be processed in Power BI."""

    query = """
    SELECT b.id, b.datum, b.beschrijving, b.lat, b.lon, c.capcode
    FROM Bericht b
    LEFT JOIN BerichtCapcode bc ON b.id = bc.bericht_id
    LEFT JOIN Capcode c ON bc.capcode_id = c.id
    """

    df = pd.read_sql_query(query, cursor.connection)

    # Handle NaN values for lat and lon
    df['lat'] = df['lat'].fillna('NaN')
    df['lon'] = df['lon'].fillna('NaN')

    df.to_csv("exports/" + filename, index=False)
    print(f"Data exported to {filename}")


conn = SQLServer.connect("P2000")
cursor = conn.cursor()

export_to_csv(cursor, 'test.csv')
