import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Iterable
from dotenv import load_dotenv

class Database:
    load_dotenv()
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME", "codebase"),
        user=os.getenv("DB_USER", "postgres"),
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=os.getenv("DB_PORT", "5432")
    )
    connection.autocommit = True

    def __init__(self, table: str):
        self.table = table

    def count(self, query: str = "1=1") -> int:
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {self.table} WHERE {query}")
            return cursor.fetchone()[0]

    def search(self, search: str) -> list[dict]:
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(f"SELECT * FROM {self.table} WHERE to_tsvector('english', column_name) @@ plainto_tsquery('english', %s)", (search,))
            return cursor.fetchall()

    def find(self, query: str = "1=1") -> list[dict]:
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(f"SELECT * FROM {self.table} WHERE {query}")
            return cursor.fetchall()

    def find_one(self, query: str = "1=1") -> dict:
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(f"SELECT * FROM {self.table} WHERE {query} LIMIT 1")
            return cursor.fetchone()

    def write_one(self, record: dict):
        with self.connection.cursor() as cursor:
            columns = ', '.join(record.keys())
            values = ', '.join(['%s'] * len(record))
            cursor.execute(f"INSERT INTO {self.table} ({columns}) VALUES ({values}) RETURNING id", tuple(record.values()))
            return cursor.fetchone()[0]

    def write_many(self, records: Iterable[dict]):
        if not records:
            return
        with self.connection.cursor() as cursor:
            columns = ', '.join(records[0].keys())
            values = ', '.join(['%s'] * len(records[0]))
            args = [tuple(record.values()) for record in records]
            cursor.executemany(f"INSERT INTO {self.table} ({columns}) VALUES ({values})", args)

    def update_one(self, query: str, update: dict):
        with self.connection.cursor() as cursor:
            set_clause = ', '.join([f"{k} = %s" for k in update.keys()])
            cursor.execute(f"UPDATE {self.table} SET {set_clause} WHERE {query}", tuple(update.values()))

    def delete_one(self, query: str):
        with self.connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {self.table} WHERE {query} LIMIT 1")

    def delete_many(self, query: str):
        with self.connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {self.table} WHERE {query}")

    def reset_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute(f"TRUNCATE TABLE {self.table} RESTART IDENTITY")

    def make_index(self, column: str):
        with self.connection.cursor() as cursor:
            cursor.execute(f"CREATE INDEX IF NOT EXISTS {self.table}_{column}_idx ON {self.table} USING gin(to_tsvector('english', {column}))")

    def drop_index(self, column: str):
        with self.connection.cursor() as cursor:
            cursor.execute(f"DROP INDEX IF EXISTS {self.table}_{column}_idx")
