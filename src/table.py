import pandas as pd
import os


# refactor to instantiate once per output csv (3 times)
class Table:
    open_positions_cols = [
        "account_id",
        "order_id",
        "open_time",
        "type",
        "size",
        "amount_k",
        "symbol",
        "entry_price",
        "sl",
        "tp",
        "current_price",
        "swap",
        "pl",
    ]

    accounts_cols = [
        "broker",
        "account_id",
        "account_name",
        "balance",
        "margin",
        "pl",
    ]

    def __init__(self, path) -> None:
        self.csv_path = path
        self.existing_table = self.load_csv(self.csv_path)

    def load_csv(self, path):
        if os.path.isfile(path):
            df = pd.read_csv(path)
            return df
        else:
            return pd.DataFrame()

    def write_csv(self, table, account_id):
        new_table = table
        if not self.existing_table.empty:
            other_accounts = self.existing_table[
                self.existing_table.account_id != account_id
            ]
            new_table = pd.concat([other_accounts, table], ignore_index=True)
            new_table = new_table.sort_values(by=["account_id"])

        new_table.to_csv(self.csv_path, sep=",", index=False)
    
    def write_csv_new(self, data):
        table = pd.concat(data, ignore_index=True)
        table = table.sort_values(by=["account_id"])
        table.to_csv(self.csv_path, sep=",", index=False)
