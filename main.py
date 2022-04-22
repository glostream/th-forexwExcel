import pandas as pd
from src.fxcm import Fxcm
from src.db import Db


def main():
    db = Db()
    db.list_tables()

    fxcm = Fxcm()
    positions = fxcm.getPositions()
    db.save_open_positions(positions)

    db.execSql('''SELECT * FROM open_positions''')


if __name__ == "__main__":
    main()
