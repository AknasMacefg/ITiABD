import psycopg2

def create_tables(conn):
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Магазины (
            Номер SERIAL PRIMARY KEY,
            Адрес VARCHAR(255),
            Телефон VARCHAR(20),
            ФИО VARCHAR(100),
            Количество_сотрудников INTEGER
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Техника (
            Код SERIAL PRIMARY KEY,
            Название VARCHAR(100),
            Марка VARCHAR(50),
            Масса INTEGER,
            Цена NUMERIC
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS НаличиеТехники (
            Магазин INTEGER REFERENCES Магазины(Номер) ON DELETE CASCADE,
            Техника INTEGER REFERENCES Техника(Код) ON DELETE CASCADE,
            Количество INTEGER,
            PRIMARY KEY (Магазин, Техника)
        );
    """)

    conn.commit()                  
    cur.close()

def add_product(conn, name, brand, mass, price):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Техника (Код, Название, Марка, Масса, Цена)
            VALUES (default, %s, %s, %s, %s);
        """, (name, brand, mass, price))
    conn.commit()

def add_all_products(conn):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Техника
            VALUES (1,'Холодильник','Samsung',50,12500),
                   (2,'Пылесос','Bosch',5,6200),
                   (3,'Мультиварка','Samsung',10,17800),
                   (4,'Робот-пылесос','Samsung',5,25000),
                   (5,'Мясорубка','Bosch',3,2300),
                   (6,'Телевизор','LG',30,100000),
                   (7,'Музыкальный центр','Pioneer',null,8000),
                   (8,'Миксер','Braun',2,1500),
                   (9,'Стиральная машина','Ariston',3,12500),
                   (10,'СВЧ-печь','Braun',6,3000);
        """)
    conn.commit()

def add_store(conn, address, phone, director, employees_count):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Магазины(Адрес, Телефон, ФИО, Количество_сотрудников)
            VALUES (%s, %s, %s, %s);
        """, (address, phone, director, employees_count))
    conn.commit()

def add_all_stores(conn):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Магазины
            VALUES (1, 'Гагарина, 34',	'112233', 'Лапин М.К.', 50),
                   (2, 'Народный бульвар, 12',	'223311', 'Морозов К.Л.', 30),
                   (3, 'Ленина, 18', '443322', 'Калинина Ю.Д.', 45),
                   (4, 'Зубковой, 56',	'772233', 'Шац П.А.', 60),
                   (5, 'Циолковского, 43а', '225533', 'Кокеткина И.Н.', 35),
                   (6, 'Московское шоссе, 76',	'225544', 'Барсов Р.К.', 75),
                   (7, 'Грибоедова, 1', '555555', 'Васильев М.Т.', 45),
                   (8, 'Интернациональная, 12', '771122', 'Гагарин Ю.Д.', 50),
                   (9, 'Колхозная, 33', '553344', 'Кратер Р.П.', 30),
                   (10, 'Западная, 12', '445566', 'Савельев П.Н.', 45);
        """)
    conn.commit()

def add_inventory(conn, store_code, product_code, amount):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO НаличиеТехники (Магазин, Техника, Количество)
            VALUES (%s, %s, %s);
        """, (store_code, product_code, amount))
    conn.commit()


def add_all_inventory(conn):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO НаличиеТехники
            VALUES (1,1,40),
                   (1,8,25),
                   (2,5,45),
                   (2,6,30),
                   (2,8,15),
                   (3,1,50),
                   (3,6,20),
                   (3,7,15),
                   (5,2,42),
                   (5,5,35),
                   (6,1,45),
                   (6,10,10),
                   (7,4,25),
                   (7,8,25),
                   (8,1,15),
                   (8,3,50),
                   (8,4,62),
                   (9,8,21),
                   (10,1,30),
                   (10,10,20);
        """)
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

conn = psycopg2.connect(dbname="SUBD_PR9", user="postgres", password="postgres", host="localhost")
#create_tables(conn)
#add_all_stores(conn)
#add_all_products(conn)
#add_all_inventory(conn)
add_store(conn, 'Пушкино, 23', '123456', 'Гагаренко И.И', 24)
add_product(conn, 'Мультиварка', 'Sony', 4, 5000)
add_inventory(conn,11, 4, 50)
conn.close()