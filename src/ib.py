from decimal import ROUND_HALF_DOWN
from src.table import Table
import pandas as pd

# from ibw.client import IBClient
import requests

try:
    from keys.keys import IB as creds
except Exception as e:
    print(e)
    raise "could not find FXCM API key in keys/keys.py"


class Ib:
    def __init__(self):
        # This is NOT the account id that is used in account endpoints
        self.account_number = creds["paper_account_number"]
        self.base_api_bath = "https://localhost:5001/v1"
        self.connect()

    def get_api(self, path):
        try:
            r = requests.get(f"{self.base_api_bath}{path}", verify=False)
        except Exception as e:
            print(f"request failed. ERROR {e}")
        if r.status_code == 401:
            print(f"requst failed. User is not authenticated")
            return {}
        elif r.status_code != 200:
            print(f"request failed ERROR code {r.status_code} and message {r.text}")
            return {}
        return r.json()

    def connect(self):
        print("connecting to IB API...")
        print("please go to this URL and login: https://localhost:5001/")
        print("please hit enter/return when complete")
        input("")

        r = self.get_api("/portal/sso/validate")

        print(f"connected to IB API with credentials:\n{r}")
        # # raise timeout error if connection takes too long
        # self.con = IBClient(
        #     username=creds["paper_username"],
        #     account=creds["paper_account_number"],
        #     # is_server_running=True,
        # )
        # self.con.create_session()

    def get_account(self, accounts_table):
        data = ["IB", self.account_id]

        r = self.get_api(f"/portfolio/accounts")
        if r:
            self.account_id = r[0]["id"]
            data.append(r["displayName"])

        r = self.get_api(f"/portfolio/{self.account_id}/summary")
        # if r:
        # for i in [data.append()
        try:
            accounts = self.con.portfolio_accounts()
        except Exception as e:
            print(e)
            return accounts_table.existing_table[
                accounts_table.existing_table.account_id == self.account_id
            ]

        print(accounts)
        # generate additional columns
        # accounts_db = accounts[cols].copy()
        # accounts_db.insert(0, "broker", ["IB"] * len(accounts_db.index))
        # accounts_db.columns = [Table.accounts_cols]
        # accounts_db.columns = accounts_db.columns.get_level_values(0)

        # return accounts_db

    def get_positions(self, positions_table):
        cols = [
            "dealId",
            "createdDateUTC",
            "direction",
            "size",
            "instrumentName",
            "level",
            "stopLevel",
            "limitLevel",
        ]

        try:
            positions = self.con.fetch_open_positions()
        except Exception as e:
            print(e)
            return positions_table.existing_table[
                positions_table.existing_table.account_id == self.account_id
            ]

        positions_db = positions[cols].copy()

        # insert additional columns at positions to match with order of Db.open_positions_columns
        positions_db.insert(
            0, "account_id", [self.account_id] * len(positions_db.index)
        )
        positions_db.insert(5, "amount_k", positions["size"].copy())
        positions_db.insert(
            10,
            "current_price",
            positions.apply(
                lambda row: row.bid if row.direction == "SELL" else row.offer, axis=1
            ),
        )
        positions_db.insert(11, "swap", [""] * len(positions_db.index))
        positions_db.insert(
            12,
            "pl",
            positions.apply(
                lambda row: row.size * row.lotSize * row.percentageChange, axis=1
            ),
        )
        positions_db.columns = [Table.open_positions_cols]
        positions_db.columns = positions_db.columns.get_level_values(0)

        return positions_db
