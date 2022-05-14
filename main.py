from src.fxcm import Fxcm
from src.ig import Ig
from src.ib import Ib
from src.table import Table

# import xlwings as xw
import time, datetime


ACCOUNTS_PATH = "data/accounts.csv"
POSITIONS_PATH = "data/positions.csv"


def main():
    accounts_table = Table(ACCOUNTS_PATH)
    positions_table = Table(POSITIONS_PATH)

    brokers = [
        Ig(),
        Fxcm(),
        # Ib(),
    ]
    brokers = [b for b in brokers if b.is_disabled != True]
    # accounts = [b.get_account(accounts_table) for b in brokers]
    # brokers[1].open_new_position({})

    try:
        while 1:
            print(f"{datetime.datetime.now()} - fetching data...")
            accounts = [b.get_account(accounts_table) for b in brokers]
            positions = [b.get_positions(positions_table) for b in brokers]

            accounts_table.write_csv_new(accounts)
            positions_table.write_csv_new(positions)

            time.sleep(10)
    except Exception as e:
        print(f"main loop crashed ERROR {e}")
        print("restart program")


if __name__ == "__main__":
    main()
