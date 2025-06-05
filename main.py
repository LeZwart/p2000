# import SQLServer
from p2kflex import scrape_region

REGION_COUNT = 25


def main():
    # conn = SQLServer.connect()
    # cursor = conn.cursor()

    all_messages = []
    for i in range(1, REGION_COUNT + 1):
        region = f"R{i}"

        region_data = scrape_region(region)
        all_messages.extend(region_data)
        print(f"Scraped data for {region}: {len(region_data)} records")
    print(f"Total records scraped: {len(all_messages)}")


if __name__ == "__main__":
    main()
