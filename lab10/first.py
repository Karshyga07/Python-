import psycopg2
import csv
from tabulate import tabulate



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
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        phone VARCHAR(255) NOT NULL
    ); 
""")

with open('people.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cur.execute(
            "INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s);",
            (row["name"], row["surname"], row["phone"])
        )
conn.commit()
print("Добавлено")

name = input("Введите имя: ")
surname = input("Введите фамилию: ")
phone = input("Введите номер телефона: ")

cur.execute(
    "INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s);", 
    (name, surname, phone)
)
conn.commit()
print("Добавлено")


filed = input("Что вы хотите обновить? (name, surname, phone): ")
if filed == 'name':
    old_name = input("Старое имя: ")
    new_name = input("Новое имя: ")
    cur.execute(
        "UPDATE phonebook SET name = %s WHERE name = %s;", 
        (new_name, old_name)
    )
    print("Обновлено")
elif filed == 'surname':
    old_surname = input("Старая фамилия: ")
    new_surname = input("Новая фамилия: ")
    cur.execute(
        "UPDATE phonebook SET surname = %s WHERE surname = %s;", 
        (new_surname, old_surname)
    )
    print("Обновлено")
elif filed == 'phone':
    old_phone = input("Старый номер телефона: ")
    new_phone = input("Новый номер телефона: ")
    cur.execute(
        "UPDATE phonebook SET phone = %s WHERE phone = %s;", 
        (new_phone, old_phone)
    )
    print("Обновлено")
else:
    print("Неверно")

    
    
name_filter = input("Введите имя: ")
cur.execute(
    "SELECT * FROM phonebook WHERE name = %s;", 
    (name_filter,)
)
rows = cur.fetchall()
print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt="fancy_grid"))



option = input("Удалить по имени (1) или по телефону (2)? ")

if option == "1":
    name = input("Введите имя для удаления: ")
    cur.execute(
        "DELETE FROM phonebook WHERE name = %s", 
        (name,)
    )
    print(f"Удалены все записи с именем: {name}")

elif option == "2":
    phone = input("Введите телефон для удаления: ")
    cur.execute(
        "DELETE FROM phonebook WHERE phone = %s", 
        (phone,)
    )
    print(f"Удалены все записи с телефоном: {phone}")

else:
    print("Неверный выбор")


cur.execute("SELECT * from phonebook;")
rows = cur.fetchall()
print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))
conn.commit()
cur.close()
conn.close()
