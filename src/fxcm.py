from email.policy import default
from tkinter.tix import Tree
from src.table import Table
import fxcmpy

try:
    from keys.keys import FXCM as TOKEN
except Exception as e:
    print(e)
    raise "could not find FXCM API key in keys/keys.py"


class Fxcm:
    def __init__(self):
        self.account_id = 889071
        self.connect()
        self.is_disabled = False

    def connect(self):
        print("connecting to FXCM API...")
        # raise timeout error if connection takes too long
        try:
            self.con = fxcmpy.fxcmpy(access_token=TOKEN, log_level="error")
            print("connected!")
        except Exception as e:
            print(e)
            self.is_disabled = True
            print("FXCM has been DISABLED for this session")

    def open_new_position(self, params):
        defaults = {
            "symbol": "USD/JPY",
            "is_buy": True,
            "amount": 10,
            "time_in_force": "GTC",
            "order_type": "AtMarket",
            "rate": 0,
            "is_in_pips": False,
            "limit": None,
            "at_market": 0,
            "stop": None,
            "trailing_step": None,
            "account_id": None,
        }
        self.con.open_trade(**defaults)

    def get_account(self, accounts_table):
        cols = ["accountId", "balance", "usableMargin", "grossPL"]

        try:
            accounts = self.con.get_accounts()
        except Exception as e:
            print(e)
            return accounts_table.existing_table[
                accounts_table.existing_table.account_id == self.account_id
            ]

        # generate additional columns
        accounts_db = accounts[cols].copy()
        accounts_db.insert(0, "broker", ["FXCM"] * len(accounts_db.index))
        accounts_db.insert(2, "account_name", [""] * len(accounts_db.index))
        accounts_db.columns = [Table.accounts_cols]
        accounts_db.columns = accounts_db.columns.get_level_values(0)

        return accounts_db

    def get_positions(self, positions_table):
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
            return positions_table.existing_table[
                positions_table.existing_table.account_id == self.account_id
            ]

        positions_db = positions[cols].copy()
        positions_db["time"] = positions_db["time"].apply(
            lambda x: f"{x[4:8]}-{x[0:2]}-{x[2:4]}T{x[8:10]}:{x[10:12]}:{x[12:]}"
        )

        # insert additional columns at positions to match with order of Db.open_positions_columns
        positions_db.insert(
            3, "type", positions["isBuy"].copy().apply(lambda x: "buy" if x else "sell")
        )
        positions_db.insert(4, "size", positions["amountK"].copy())
        positions_db.insert(11, "swap", [""] * len(positions_db.index))
        positions_db.columns = [Table.open_positions_cols]
        positions_db.columns = positions_db.columns.get_level_values(0)

        return positions_db
