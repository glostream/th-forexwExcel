from src.fxcm import Fxcm
from src.db import Db
import time
import pandas as pd
from src.csv import Csv

CSV_PATH = "data"


def get_fxcm(fxcm, csv):
    print("getting FXCM data...")
    account = fxcm.get_account(csv.existing_accounts)
    positions = fxcm.get_positions(csv.existing_positions)

    if not positions.empty:
        csv.write_open_positions(positions, fxcm.account_id)
    if not account.empty:
        csv.write_accounts(account, fxcm.account_id)


def main():
    # db = Db()
    # db.list_tables()
    csv = Csv(CSV_PATH)

    fxcm = Fxcm()

    for i in range(100):
        get_fxcm(fxcm, csv)
        time.sleep(5)


if __name__ == "__main__":
    main()
