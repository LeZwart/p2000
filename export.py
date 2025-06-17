import pandas as pd
import SQLServer


def export_query_to_csv(cursor, query, filename):
    """Helper to export a SQL query to CSV."""
    df = pd.read_sql_query(query, cursor.connection)
    df.to_csv("exports/" + filename, index=False)
    print(f"Exported to {filename}")


# Connect to the SQL Server database
conn = SQLServer.connect("P2000")
cursor = conn.cursor()

# Define and export each query
queries = {
    "Bericht.csv": """
        SELECT
            id AS bericht_id,
            datum,
            beschrijving,
            lat,
            lon
        FROM dbo.Bericht
    """,

    "BerichtCapcode.csv": """
        SELECT
            bericht_id,
            capcode_id
        FROM dbo.BerichtCapcode
    """,

    "Capcode.csv": """
        SELECT
            id AS capcode_id,
            capcode,
            beschrijving,
            discipline AS discipline_id,
            regio AS regio_id,
            stad AS stad_id
        FROM dbo.Capcode
    """,

    "Discipline.csv": """
        SELECT
            id AS discipline_id,
            naam AS discipline_naam
        FROM dbo.Discipline
    """,

    "Regio.csv": """
        SELECT
            id AS regio_id,
            naam AS regio_naam
        FROM dbo.Regio
    """,

    "Stad.csv": """
        SELECT
            id AS stad_id,
            naam AS stad_naam
        FROM dbo.Stad
    """
}

# Run and export all queries
for filename, query in queries.items():
    export_query_to_csv(cursor, query, filename)
