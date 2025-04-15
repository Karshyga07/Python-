import psycopg2

conn = psycopg2.connect(
    dbname = "postgres",
    user = "omega",
    password = "",
    host = "localhost",
    port = "5432"
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT,
        age INTEGER
    );
""")

cur.execute("INSERT INTO users (name, age) VALUES (%s, %s);", ("Aruzhan", 21))
cur.execute("INSERT INTO users (name, age) VALUES (%s, %s);", ("Dias", 19))

cur.execute("SELECT * FROM users;")
rows = cur.fetchall()
for row in rows:
    print(row)

conn.commit()
cur.close()
conn.close()

print("Готово! Данные добавлены и таблица выведена.")
