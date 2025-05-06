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

def add_product(conn, products):
    with conn.cursor() as cur:
        cur.executemany("""
            INSERT INTO Техника (Название, Марка, Масса, Цена)
            VALUES (%s, %s, %s, %s);
        """, products)
    conn.commit()

def add_all_products(conn):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Техника(Название, Марка, Масса, Цена)
            VALUES ('Холодильник','Samsung',50,12500),
                   ('Пылесос','Bosch',5,6200),
                   ('Мультиварка','Samsung',10,17800),
                   ('Робот-пылесос','Samsung',5,25000),
                   ('Мясорубка','Bosch',3,2300),
                   ('Телевизор','LG',30,100000),
                   ('Музыкальный центр','Pioneer',null,8000),
                   ('Миксер','Braun',2,1500),
                   ('Стиральная машина','Ariston',3,12500),
                   ('СВЧ-печь','Braun',6,3000);
        """)
    conn.commit()

def add_store(conn, stores):
    with conn.cursor() as cur:
        cur.executemany("""
            INSERT INTO Магазины(Адрес, Телефон, ФИО, Количество_сотрудников)
            VALUES (%s, %s, %s, %s);
        """, stores)
    conn.commit()

def add_all_stores(conn):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Магазины(Адрес, Телефон, ФИО, Количество_сотрудников)
            VALUES ('Гагарина, 34',	'112233', 'Лапин М.К.', 50),
                   ('Народный бульвар, 12',	'223311', 'Морозов К.Л.', 30),
                   ('Ленина, 18', '443322', 'Калинина Ю.Д.', 45),
                   ('Зубковой, 56',	'772233', 'Шац П.А.', 60),
                   ('Циолковского, 43а', '225533', 'Кокеткина И.Н.', 35),
                   ('Московское шоссе, 76',	'225544', 'Барсов Р.К.', 75),
                   ('Грибоедова, 1', '555555', 'Васильев М.Т.', 45),
                   ('Интернациональная, 12', '771122', 'Гагарин Ю.Д.', 50),
                   ('Колхозная, 33', '553344', 'Кратер Р.П.', 30),
                   ('Западная, 12', '445566', 'Савельев П.Н.', 45);
        """)
    conn.commit()

def add_inventory(conn, inventories):
    with conn.cursor() as cur:
        cur.executemany("""
            INSERT INTO НаличиеТехники(Магазин, Техника, Количество)
            VALUES (%s, %s, %s);
        """, inventories)
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


def get_all(conn, table):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM " + table + ";")
        return cur.fetchall()

def get_one_by_name(conn, table, column, target):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM "+ table +" WHERE "+ column + " = %s;", (target,))
        return cur.fetchone()

def get_inventory_by_store(conn, id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT s.Адрес, p.Название, i.Количество
            FROM НаличиеТехники i
            JOIN Магазины s ON i.Магазин = s.Номер
            JOIN Техника p ON i.Техника = p.Код
            WHERE s.Номер = %s;
        """, (id,))
        return cur.fetchall()

def update_product_price(conn, product_id, new_price):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE Техника
            SET Цена = %s
            WHERE Код = %s;
        """, (new_price, product_id))
    conn.commit()

def update_store_employees(conn, store_id, new_count):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE Магазины
            SET Количество_сотрудников = %s
            WHERE Номер = %s;
        """, (new_count, store_id))
    conn.commit()

def update_inventory_amount(conn, store_id, product_id, new_count):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE НаличиеТехники
            SET Количество = %s
            WHERE Магазин = %s AND Техника = %s;
        """, (new_count, store_id, product_id))
    conn.commit()    

def delete_store_by_id(conn, store_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM Магазины WHERE Номер = %s;", (store_id,))
    conn.commit()

def delete_all_stores(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM Магазины;")
    conn.commit()

def delete_product_by_id(conn, product_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM Техника WHERE Код = %s;", (product_id,))
    conn.commit()

def delete_all_products(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM Техника;")
    conn.commit()

def delete_inventory_by_id(conn, store_id, product_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM НаличиеТехники WHERE Магазин = %s AND Техника = %s;", (store_id, product_id))
    conn.commit()

def delete_all_inventories(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM НаличиеТехники;")
    conn.commit()

conn = psycopg2.connect(dbname="SUBD_PR9", user="postgres", password="postgres", host="localhost")
#create_tables(conn)
#add_all_stores(conn)
#add_all_products(conn)
#add_all_inventory(conn)
#add_store(conn, [('Пушкино, 23', '123456', 'Гагаренко И.И', 24)])
#add_product(conn, [('Мультиварка', 'Sony', 4, 5000), ('Пароварка', 'Bosch', 5, 10000)])
#add_inventory(conn,[(11, 4, 50)])
#print(get_all(conn, "Техника"))
#print(get_one_by_name(conn, "Магазины", "Номер", 1))
#print(get_inventory_by_store(conn, 1))
#update_inventory_amount(conn, 1, 1, 50)
#update_product_price(conn, 1, 10000)
#update_store_employees(conn, 1, 30)
#delete_inventory_by_id(conn, 1, 1)
#delete_product_by_id(conn, 1)
#delete_store_by_id(conn, 1)
#delete_all_inventories(conn)
#delete_all_products(conn)
#delete_all_stores(conn)
conn.close()