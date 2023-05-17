import psycopg2
from sc import secret


def insert_item(article, name, image):
    conn = psycopg2.connect(
        host=secret.DATABASE_HOST,
        database=secret.DATABASE_NAME,
        user=secret.DATABASE_LOGIN,
        password=secret.DATABASE_PASSWORD,
    )
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {'ozon_items'} (article, image, name, pack_type) "
                f"SELECT %s, %s, %s, %s WHERE NOT EXISTS "
                f"(SELECT article FROM {'ozon_items'} WHERE article = %s)",
                (str(article), image, name, '', str(article)))
    conn.commit()
    conn.close()


def update_pack_type(article, pack_type):
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

