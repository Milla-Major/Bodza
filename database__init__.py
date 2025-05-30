import sqlite3

conn = sqlite3.connect("magazine_subscription.db")
cursor = conn.cursor()

def create_mydatabase():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS magazine (
        magazine_id INTEGER PRIMARY KEY,
        type_code INTEGER CHECK(type_code IN (1, 2, 3, 4)),
        title TEXT NOT NULL,
        publisher TEXT NOT NULL,
        monthly_fee INTEGER CHECK(monthly_fee >= 1 AND monthly_fee < 50)
    );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subscriber (
        subscriber_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        birth_date,
        postal_code INTEGER CHECK(postal_code BETWEEN 1000 AND 9999),
        city TEXT,
        street TEXT
    );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subscription (
        subscriber_id INTEGER,
        magazine_id INTEGER,
        start_date DATE DEFAULT CURRENT_DATE,
        end_date DATE,
        quantity INTEGER CHECK(quantity > 0 AND quantity < 1000),
        PRIMARY KEY (subscriber_id, magazine_id),
        FOREIGN KEY (subscriber_id) REFERENCES subscriber(subscriber_id),
        FOREIGN KEY (magazine_id) REFERENCES magazine(magazine_id)
    );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL
    );
    ''')
    print("database created")


def add_testdata():
    #region adding test data
    cursor.executemany('''
    INSERT INTO magazine (magazine_id, type_code, title, publisher, monthly_fee)
    VALUES (?, ?, ?, ?, ?);
    ''', [
        (1, 1, "Daily News", "Daily Press Ltd.", 10),
        (2, 3, "Science Monthly", "SciPub Inc.", 20),
        (3, 2, "Family Life", "Home & Family Co.", 15)
    ])
    cursor.executemany('''
    INSERT INTO subscriber (subscriber_id, name, birth_date, postal_code, city, street)
    VALUES (?, ?, ?, ?, ?, ?);
    ''', [
        (100, "Alice Johnson", "1990-05-20", 1234, "Amsterdam", "Tulipstraat 12"),
        (101, "Bob de Vries", "1985-10-03", 2345, "Rotterdam", "Kerklaan 7"),
        (102, "Carla van Dijk", "1978-01-15", 3456, "Utrecht", "Singel 44")
    ])
    cursor.executemany('''
    INSERT INTO subscription (subscriber_id, magazine_id, start_date, end_date, quantity)
    VALUES (?, ?, ?, ?, ?);
    ''', [
        (100, 1, "2024-01-01", "2024-12-31", 1),
        (101, 2, "2024-06-01", "2025-05-31", 2),
        (102, 3, "2024-03-15", "2024-09-15", 1)
    ])
    #endregion
    print("data added")

create_mydatabase()
add_testdata()
conn.commit()
conn.close()


