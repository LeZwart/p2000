import subprocess
import SQLServer

conn = ["rtl_fm", "-f", "169.65M", "-s", "22050", "-g", "50"]
decoder = ["multimon-ng", "-a", "FLEX", "-t", "raw", "-"]
db_conn = SQLServer.connect("P2000")


def parse_melding(raw_melding):
    parts = raw_melding.strip().split("|")
    if len(parts) != 7:
        raise ValueError(
            f"Invalid melding format: length = {len(parts)} '{parts}'"
        )
    return {
        "date": parts[1],
        "description": parts[6],
        "capcodes": parts[4].split()
    }


def add_capcode_to_db(capcode):
    pass


def main():
    rtl_fm_proc = subprocess.Popen(
        conn, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    multimon_proc = subprocess.Popen(
        decoder,
        stdin=rtl_fm_proc.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    while True:
        melding = multimon_proc.stdout.readline()
        if melding:
            try:
                parsed_melding = parse_melding(melding)
                print(f"Date: {parsed_melding['date']}")
                print(f"Description: {parsed_melding['description']}")
                capcodes = [
                    capcode[2:] for capcode in parsed_melding['capcodes']
                ]

                for capcode in capcodes:
                    stmt = f"SELECT * FROM Capcode WHERE capcode = '{capcode}'"

                    cursor = db_conn.cursor()
                    cursor.execute(stmt)
                    result = cursor.fetchone()
                    if not result:
                        print(f"Capcode {capcode} not found in database.")
                    else:
                        print(
                            (f"{result[1]} {result[2]} {result[3]} "
                             f"{result[4]} | {result[5]}")
                        )

                print("-"*50)
            except ValueError:
                pass


if __name__ == "__main__":
    main()
