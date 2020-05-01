import sqlite3

conn = sqlite3.connect("test.db")  #연결되어있는 db자체

cur = conn.cursor()   #cur 는 소통할수 있는 커서객체

query = """
    CREATE TABLE IF NOT EXISTS board(
        'idx' INTEGER PRIMARY KEY AUTOINCREMENT,
        'writer' VARCHAR(100),
        'title' VARCHAR(250),
        'contents' TEXT 
    )
"""

cur.execute(query)