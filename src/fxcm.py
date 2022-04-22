import fxcmpy
import requests

try:
    from keys.keys import FXCM as TOKEN
except Exception as e:
    print(e)
    raise "could not find FXCM API key in keys/keys.py"


class Fxcm:
    def __init__(self):
        self.connect()
        self.open_position_cols = [
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

    def connect(self):
        print("connecting to FXCM API...")
        self.con = fxcmpy.fxcmpy(access_token=TOKEN, log_level="error")
        print("connected to FXCM API!")

    def getApi(self):
        pass

    def getPositions(self):
        positions = self.con.get_open_positions().T
        positions = positions.transpose()
        positions_db = positions[self.open_position_cols]
        positions_db['type'] = positions['isBuy'].copy().apply(lambda x : 'buy' if x else 'sell')

        return positions_db
