
from sc import secret
import psycopg2
import dataclasses


def get_pack_type_by_article(article):
    conn = psycopg2.connect(
        host=secret.DATABASE_HOST,
        database=secret.DATABASE_NAME,
        user=secret.DATABASE_LOGIN,
        password=secret.DATABASE_PASSWORD,
    )
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM ozon_items WHERE article=%s",
                (str(article), ))
    el = cur.fetchone()
    conn.close()
    try:
        print(el[0])
        return el[0]
    except:
        return el

class Database:
    def __init__(self):
        self.table_name = secret.MODE
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

    def get_count_nakleiki(self):
        self.conn = psycopg2.connect(
            host=secret.DATABASE_HOST,
            database=secret.DATABASE_NAME,
            user=secret.DATABASE_LOGIN,
            password=secret.DATABASE_PASSWORD,
        )
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT COUNT(*) FROM ozon_items LIMIT 1;")
        record = self.cur.fetchone()
        self.conn.close()
        return record[0]

    def get_items(self, from_element: int):
        self.conn = psycopg2.connect(
            host=secret.DATABASE_HOST,
            database=secret.DATABASE_NAME,
            user=secret.DATABASE_LOGIN,
            password=secret.DATABASE_PASSWORD,
        )
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM kamran WHERE stage = %s LIMIT %s OFFSET %s;", ('Suggested', 25, from_element))
        records = self.cur.fetchall()
        self.conn.close()
        return records

    def get_suggestion_stats(self):
        self.conn = psycopg2.connect(
            host=secret.DATABASE_HOST,
            database=secret.DATABASE_NAME,
            user=secret.DATABASE_LOGIN,
            password=secret.DATABASE_PASSWORD,
        )
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM kamran WHERE stage = %s;", ('Suggested',))
        records = self.cur.fetchall()
        self.conn.close()
        return records


    def get_nakleiki(self, from_element: int):
        self.conn = psycopg2.connect(
            host=secret.DATABASE_HOST,
            database=secret.DATABASE_NAME,
            user=secret.DATABASE_LOGIN,
            password=secret.DATABASE_PASSWORD,
        )
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT * FROM ozon_items LIMIT %s OFFSET %s;", (25, from_element))
        records = self.cur.fetchall()
        self.conn.close()
        return records

    def update_nakleiki(self, article, pack_type):
        conn = psycopg2.connect(
            host=secret.DATABASE_HOST,
            database=secret.DATABASE_NAME,
            user=secret.DATABASE_LOGIN,
            password=secret.DATABASE_PASSWORD,
        )
        cur = conn.cursor()
        cur.execute(f"UPDATE {'ozon_items'} SET pack_type=%s WHERE article=%s",
                    (pack_type, article))
        conn.commit()
        conn.close()



