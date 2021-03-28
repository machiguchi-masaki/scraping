import sqlite3

conn = sqlite3.connect('data/ebook.db')

c = conn.cursor()

c.execute('select * from cities')
for row in c.fetchall():
    print(row)
    print(123)
conn.close()
