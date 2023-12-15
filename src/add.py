import sqlite3

con = sqlite3.connect("tutorial.db")

with con.cursor() as cur:
    cur.execute("SELECT a From t where col="+ input())