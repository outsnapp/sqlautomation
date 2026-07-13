import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "sample.db"


def create_database():
    DATABASE_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.executescript(
        """
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );

        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        );

        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            revenue REAL NOT NULL,
            order_date DATE NOT NULL,

            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
        """
    )

    customers = [
        ("Rahul Sharma", "India", "rahul@example.com"),
        ("Priya Patel", "India", "priya@example.com"),
        ("John Smith", "USA", "john@example.com"),
        ("Emma Wilson", "UK", "emma@example.com"),
        ("Arjun Reddy", "India", "arjun@example.com"),
        ("Michael Brown", "USA", "michael@example.com"),
        ("Sophia Lee", "Singapore", "sophia@example.com"),
        ("David Miller", "Germany", "david@example.com"),
    ]

    cursor.executemany(
        """
        INSERT INTO customers (name, country, email)
        VALUES (?, ?, ?)
        """,
        customers,
    )

    products = [
        ("Laptop", "Electronics", 80000),
        ("Smartphone", "Electronics", 50000),
        ("Headphones", "Accessories", 5000),
        ("Smart Watch", "Wearables", 15000),
        ("Keyboard", "Accessories", 3000),
    ]

    cursor.executemany(
        """
        INSERT INTO products (name, category, price)
        VALUES (?, ?, ?)
        """,
        products,
    )

    orders = [
        (1, 1, 1, 80000, "2024-01-15"),
        (2, 2, 2, 100000, "2024-01-20"),
        (3, 1, 1, 80000, "2024-02-10"),
        (4, 4, 3, 45000, "2024-02-18"),
        (5, 2, 1, 50000, "2024-03-05"),
        (1, 3, 4, 20000, "2024-03-12"),
        (6, 1, 2, 160000, "2024-04-10"),
        (7, 4, 2, 30000, "2024-04-20"),
        (8, 5, 5, 15000, "2024-05-15"),
        (2, 1, 1, 80000, "2024-06-01"),
        (5, 3, 3, 15000, "2024-06-18"),
        (3, 2, 2, 100000, "2024-07-10"),
    ]

    cursor.executemany(
        """
        INSERT INTO orders (
            customer_id,
            product_id,
            quantity,
            revenue,
            order_date
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        orders,
    )

    connection.commit()
    connection.close()

    print(f"Database created successfully at: {DATABASE_PATH}")


if __name__ == "__main__":
    create_database()