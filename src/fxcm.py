import fxcmpy
from src.db import Db
from src.csv import Csv
import pandas as pd

try:
    from keys.keys import FXCM as TOKEN
except Exception as e:
    print(e)
    raise "could not find FXCM API key in keys/keys.py"


class Fxcm:
    def __init__(self):
        self.connect()
        self.account_id = 889071

    def connect(self):
        print("connecting to FXCM API...")
        # raise timeout error if connection takes too long
        self.con = fxcmpy.fxcmpy(access_token=TOKEN, log_level="error")
        print("connected to FXCM API!")

    def getApi(self):
        pass

    def get_account(self, existing_accounts):
        cols = ["accountId", "balance", "usableMargin", "grossPL"]

        try:
            accounts = self.con.get_accounts()
        except Exception as e:
            print(e)
            return existing_accounts

        # generate additional columns
        accounts_db = accounts[cols].copy()
        accounts_db.insert(0, "broker", ["FXCM"] * len(accounts_db.index))
        accounts_db.insert(2, "account_name", [""] * len(accounts_db.index))
        accounts_db.columns = [Csv.accounts_cols]

        return accounts_db

    def get_positions(self, existing_positions):
        cols = [
            "accountId",
            "tradeId",
            "time",
            "amountK",
            "currency",
            "open",
            "stop",
            "limit",
            "close",
            "grossPL",
        ]

        try:
            positions = self.con.get_open_positions()
        except Exception as e:
            print(e)
            return existing_positions

        positions_db = positions[cols].copy()
        positions_db["time"] = positions_db["time"].apply(
            lambda x: f"{x[2:4]}-{x[0:2]}-{x[4:8]}"
        )

        # insert additional columns at positions to match with order of Db.open_positions_columns
        positions_db.insert(
            3, "type", positions["isBuy"].copy().apply(lambda x: "buy" if x else "sell")
        )
        positions_db.insert(4, "size", positions["amountK"].copy())
        positions_db.insert(11, "swap", [""] * len(positions_db.index))
        positions_db.columns = [Csv.open_positions_cols]

        return positions_db
