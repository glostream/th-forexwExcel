from src.table import Table
from trading_ig import IGService

# https://trading-ig.readthedocs.io/en/latest/


try:
    from keys.keys import IG as creds
except Exception as e:
    print(e)
    raise "could not find FXCM API key in keys/keys.py"


class Ig:
    def __init__(self):
        self.account_id = creds["account_id"]
        self.is_disabled = False
        self.connect()

    def connect(self):
        print("connecting to IG API...")
        # raise timeout error if connection takes too long
        try:
            self.con = IGService(
                creds["username"],
                creds["password"],
                creds["key"],
                creds["account_type"],
                creds["account_id"],
            )
            self.con.create_session()
            print("connected!")
        except Exception as e:
            print(e)
            self.is_disabled = True
            print("IG has been DISABLED for this session")

    def open_new_position(self, params):
        defaults = {
            "currency_code": "GBP",
            "direction": "BUY",
            "epic": "CS.D.EURGBP.CFD.IP",
            "order_type": "MARKET",
            "expiry": "-",
            "force_open": "false",
            "guaranteed_stop": "false",
            "size": 1,
            "level": None,
            "limit_distance": None,
            "limit_level": None,
            "quote_id": None,
            "stop_level": None,
            "stop_distance": None,
            "trailing_stop": None,
            "trailing_stop_increment": None,
        }
        for k, v in params.items():
            defaults[k] = v
        # params = {*defaults, params}
        r = self.con.create_open_position(**defaults)
        print(r)

    def get_account(self, accounts_table):
        cols = ["accountId", "accountName", "balance", "deposit", "profitLoss"]

        try:
            accounts = self.con.fetch_accounts()
        except Exception as e:
            print(e)
            return accounts_table.existing_table[
                accounts_table.existing_table.account_id == self.account_id
            ]

        # generate additional columns
        accounts_db = accounts[cols].copy()
        accounts_db.insert(0, "broker", ["IG"] * len(accounts_db.index))
        accounts_db.columns = [Table.accounts_cols]
        accounts_db.columns = accounts_db.columns.get_level_values(0)

        return accounts_db

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
                lambda row: row.offer if row.direction == "SELL" else row.bid, axis=1
            ),
        )
        positions_db.insert(11, "swap", [""] * len(positions_db.index))
        positions_db.insert(
            12,
            "pl",
            positions.apply(
                lambda row: round((row.level - row.offer) * row.contractSize, 2)
                if row.direction == "SELL"
                else round((row.bid - row.level) * row.contractSize, 2),
                axis=1,
            ),
        )
        positions_db.columns = [Table.open_positions_cols]
        positions_db.columns = positions_db.columns.get_level_values(0)

        return positions_db
