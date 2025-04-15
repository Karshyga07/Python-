import psycopg2
import csv


conn = psycopg2.connect(
    dbname = "postgres",
    user = "omega",
    password = "",
    host = "localhost",
    port = "5432"
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255), NOT NULL,
        surname VARCHAR(255), NOT NULL,
        phone VARCHAR(255), NOT NULL,
    );
""")
data = [
    ['name', 'surname', 'phone'],
    ['Aruzhan', 'Aitkali', '87012345678'],
    ['Dias', 'Aitkali', '87012345678'],
    ['Assem', 'Aitkali', '87012345678'],
    ['Aruzhan', 'Aitkali', '87012345678'],
    ['Dias', 'Aitkali', '87012345678'],
    ['Assem', 'Aitkali', '87012345678'],
    ['Aruzhan', 'Aitkali', '87012345678'],
    ['Dias', 'Aitkali', '87012345678'],
    ['Assem', 'Aitkali', '87012345678']
]
with open('phonebook.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
