import pandas as pd
import os


# refactor to instantiate once per output csv (3 times)
class Csv:
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
        self.path = path
        self.accounts_path = f"{self.path}/accounts.csv"
        self.open_positions_path = f"{self.path}/positions.csv"
        self.existing_accounts = self.load_csv(self.accounts_path)
        self.existing_positions = self.load_csv(self.open_positions_path)

    def load_csv(self, path):
        if os.path.isfile(path):
            df = pd.read_csv(path)
            return df
        else:
            return pd.DataFrame()

    def write_open_positions(self, positions, account_id):
        new_positions = positions
        if not self.existing_positions.empty:
            other_positions = self.existing_positions[
                self.existing_positions.account_id == account_id
            ]
            new_positions = pd.concat([other_positions, positions], ignore_index=True)
            new_positions = new_positions.sort_values(by=["account_id"])

        new_positions.to_csv(self.open_positions_path, sep=",", index=False)

    def write_accounts(self, accounts, account_id):
        new_accounts = accounts
        if not self.existing_accounts.empty:
            other_accounts = self.existing_accounts[
                self.existing_accounts.account_id == account_id
            ]
            new_accounts = pd.concat([other_accounts, accounts], ignore_index=True)
            new_accounts = new_accounts.sort_values(by=["account_id"])

        new_accounts.to_csv(self.accounts_path, sep=",", index=False)
