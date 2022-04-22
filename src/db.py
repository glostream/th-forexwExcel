import sqlite3


class Db:
    def __init__(self) -> None:
        self.connect()
        self.create_open_positions_table()

    def connect(self):
        self.con = sqlite3.connect("data.db")
        self.cur = self.con.cursor()

    def create_open_positions_table(self):
        sql = """CREATE TABLE [IF NOT EXISTS] open_positions
        account_id INT
        order_id INT
        open_time TEXT
        type TEXT
        size INT
        amount_k INT
        symbol TEXT
        entry_price REAL
        sl REAL
        tp REAL
        current_price REAL
        swap TEXT
        pl REAL
        """
        self.cur.execute(sql)
        self.con.commit()

    def list_tables(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(self.cur.fetchall())

    def save_open_positions(self, positions):
        positions.to_sql("open_positions", self.con, if_exists="appemd")

    def execSql(self, sql):
        self.cur.execute(sql)
        print(self.cur.fetchall())
