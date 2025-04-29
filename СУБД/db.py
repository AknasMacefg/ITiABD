import psycopg2

def create_tables():
    conn = psycopg2.connect(dbname="your_db", user="your_user", password="your_password", host="localhost")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            id SERIAL PRIMARY KEY,
            address VARCHAR(255),
            phone VARCHAR(20),
            director VARCHAR(100),
            employees_count INTEGER
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            brand VARCHAR(50),
            weight INTEGER,
            price NUMERIC
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            store_id INTEGER REFERENCES stores(id) ON DELETE CASCADE,
            product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
            quantity INTEGER,
            PRIMARY KEY (store_id, product_id)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

def add_store(conn, store):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO stores (address, phone, director, employees_count)
            VALUES (%s, %s, %s, %s);
        """, store)
    conn.commit()

def add_all_stores(conn, stores):
    with conn.cursor() as cur:
        cur.executemany("""
            INSERT INTO stores (address, phone, director, employees_count)
            VALUES (%s, %s, %s, %s);
        """, stores)
    conn.commit()

def get_all_stores(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM stores;")
        return cur.fetchall()

def get_store_by_phone(conn, phone):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM stores WHERE phone = %s;", (phone,))
        return cur.fetchone()

def get_inventory_by_store(conn, store_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT s.address, p.name, i.quantity
            FROM inventory i
            JOIN stores s ON i.store_id = s.id
            JOIN products p ON i.product_id = p.id
            WHERE s.id = %s;
        """, (store_id,))
        return cur.fetchall()

def update_store_employees(conn, store_id, new_count):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE stores
            SET employees_count = %s
            WHERE id = %s;
        """, (new_count, store_id))
    conn.commit()

def delete_store_by_id(conn, store_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM stores WHERE id = %s;", (store_id,))
    conn.commit()

def delete_all_stores(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM stores;")
    conn.commit()

if __name__ == "__main__":
    conn = psycopg2.connect(dbname="your_db", user="your_user", password="your_password", host="localhost")
    create_tables()

    stores = [
        ("Gagarina, 34", "112233", "Lapin M.N.", 50),
        ("Narodnyi bulvar, 12", "223311", "Morozov K.I.", 25),
        # и т.д.
    ]
    add_all_stores(conn, stores)

    print(get_inventory_by_store(conn, 1))
    update_store_employees(conn, 1, 60)
    delete_store_by_id(conn, 10)

    conn.close()
