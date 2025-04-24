import psycopg2
import csv
from tabulate import tabulate

conn = psycopg2.connect(
    dbname="postgres",
    user="omega",
    password="",   
    host="localhost",
    port="5432"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        phone VARCHAR(255) NOT NULL
    );
""")
conn.commit()


def insert_data():
    print('Type "csv" or "con" to choose option between uploading csv file or typing from console: ')
    method = input().lower()
    if method == "con":
        name = input("Name: ")
        surname = input("Surname: ")
        phone = input("Phone: ")
        cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (name, surname, phone))
    elif method == "csv":
        filepath = input("Enter a file path: ")
        try:
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if len(row) == 3:
                        cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", tuple(row))
        except FileNotFoundError:
            print("File not found.")
    conn.commit()

def update_data():
    valid_columns = ['name', 'surname', 'phone']
    column = input('name update (name/surname/phone): ').lower()
    if column not in valid_columns:
        print("Invalid column name")
        return
    value = input(f"Enter the current {column}: ")
    new_value = input(f"Enter the new {column}: ")
    cur.execute(f"UPDATE phonebook SET {column} = %s WHERE {column} = %s", (new_value, value))
    conn.commit()

def delete_data():
    phone = input('phone number to delete: ')
    cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    conn.commit()

def query_data():
    valid_columns = ['name', 'surname', 'phone']
    column = input("name search (name/surname/phone): ").lower()
    if column not in valid_columns:
        print("Invalid column name")
        return
    value = input(f"Enter the {column} value: ")
    cur.execute(f"SELECT * FROM phonebook WHERE {column} = %s", (value,))
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"]))
    else:
        print("No matching records found.")

def display_data():
    cur.execute("SELECT * FROM phonebook;")
    rows = cur.fetchall()
    print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))


while True:
    print("""
List of commands:
1. Type "i" to INSERT data.
2. Type "u" to UPDATE data.
3. Type "q" to QUERY specific data.
4. Type "d" to DELETE data.
5. Type "s" to SHOW all data.
6. Type "f" to FINISH the program.
    """)

    command = input("Enter your command: ").lower()

    if command == "i":
        insert_data()
    elif command == "u":
        update_data()
    elif command == "d":
        delete_data()
    elif command == "q":
        query_data()
    elif command == "s":
        display_data()
    elif command == "f":
        print("Exiting...")
        break
    else:
        print("Unknown command.")
conn.commit()
cur.close()
conn.close()