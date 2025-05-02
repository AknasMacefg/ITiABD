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
            INSERT INTO Техника (Код, Название, Марка, Масса, Цена)
            VALUES (default, %s, %s, %s, %s);
        """, products)
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

def add_inventory(conn, inventories):
    with conn.cursor() as cur:
        cur.executemany("""
            INSERT INTO НаличиеТехники (Магазин, Техника, Количество)
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

def update_product_price(conn, store_id, new_count):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE stores
            SET employees_count = %s
            WHERE id = %s;
        """, (new_count, store_id))
    conn.commit()

def update_store_employees(conn, store_id, new_count):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE stores
            SET employees_count = %s
            WHERE id = %s;
        """, (new_count, store_id))
    conn.commit()

def update_inventory_amount(conn, store_id, new_count):
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
#add_store(conn, ('Пушкино, 23', '123456', 'Гагаренко И.И', 24))
#add_product(conn, [('Мультиварка', 'Sony', 4, 5000), ('Пароварка', 'Bosch', 5, 10000)])
#add_inventory(conn,(11, 4, 50))
#print(get_all(conn, "Техника"))
#print(get_one_by_name(conn, "Магазины", "Номер", 1))
#print(get_inventory_by_store(conn, 1))
conn.close()