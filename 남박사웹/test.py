import sqlite3

conn = sqlite3.connect("test.db")  

cur = conn.cursor()   

query = """
    CREATE TABLE IF NOT EXISTS board(
        'idx' INTEGER PRIMARY KEY AUTOINCREMENT,
        'writer' VARCHAR(100),
        'title' VARCHAR(250),
        'contents' TEXT 
    )
"""

cur.execute(query)


query = "INSERT INTO board (writer, title, contents) VALUES ('Lee','sub','con') "
qurey ="SELECT writer, title,contents FROM board"
cur.execute(query)
conn.commit()
# rows = cur.fetchall()S
# for row in rows:
#     print(row)


conn.close()