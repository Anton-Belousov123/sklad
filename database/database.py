
from sc import secret
import psycopg2
import dataclasses
class Database:
    def __init__(self):
        self.table_name = 'kamran'
    def get_count(self, stage):
        self.conn = psycopg2.connect(
            host=secret.DATABASE_HOST,
            database=secret.DATABASE_NAME,
            user=secret.DATABASE_LOGIN,
            password=secret.DATABASE_PASSWORD,
        )
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT COUNT(*) FROM kamran WHERE stage=%s LIMIT 1;", (stage, ))
        record = self.cur.fetchone()
        self.conn.close()
        return record[0]

