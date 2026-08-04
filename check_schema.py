import sqlite3

conn = sqlite3.connect("seed/travel.db")
cursor = conn.cursor()

print("FLIGHTS")
cursor.execute("PRAGMA table_info(flights)")
for row in cursor.fetchall():
    print(row)

print("\nHOTELS")
cursor.execute("PRAGMA table_info(hotels)")
for row in cursor.fetchall():
    print(row)

conn.close()