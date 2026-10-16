import os
import struct
import time


# ---------- модель ----------

class User:
    __slots__ = ("id", "name", "age", "city")

    def __init__(self, id, name, age, city):
        self.id = id
        self.name = name
        self.age = age
        self.city = city

    def __repr__(self):
        return (
            f"User(id={self.id}, name={self.name!r}, "
            f"age={self.age}, city={self.city!r})"
        )


# ---------- псевдо-БД, размещённая на накопителе (SSD/HDD) ----------

class FileDB:
    """
    Псевдо-СУБД без внешних СУБД.

    Данные хранятся в бинарном файле фиксированными записями.
    Формат записи: id(int64) | name(32 байта) | age(int64) | city(32 байта).
    Рядом лежит индексный файл: (id(int64), offset(int64)) — для быстрого
    доступа по id. Индекс подгружается в память (как это делают реальные СУБД),
    а сами структуры данных читаются с диска.
    """

    RECORD_FMT = "<q32sq32s"
    RECORD_SIZE = struct.calcsize(RECORD_FMT)   # 80 байт
    IDX_FMT = "<qq"
    IDX_SIZE = struct.calcsize(IDX_FMT)         # 16 байт

    def __init__(self, data_path):
        self.data_path = data_path
        self.index_path = data_path + ".idx"
        self._df = None
        self._xf = None
        self._by_id = {}
        self._open()

    # ---- служебное ----

    def _open(self):
        fresh = not os.path.exists(self.data_path)
        self._df = open(self.data_path, "w+b" if fresh else "r+b")

        if fresh or not os.path.exists(self.index_path):
            self._xf = open(self.index_path, "w+b")
            self._rebuild_index()
        else:
            self._xf = open(self.index_path, "r+b")

        self._load_index()

    def _rebuild_index(self):
        """Строит индексный файл, сканируя файл данных (на случай сбоя)."""
        self._xf.seek(0)
        self._xf.truncate(0)
        self._df.seek(0, 2)
        total = self._df.tell()
        self._df.seek(0)
        offset = 0
        while offset + self.RECORD_SIZE <= total:
            chunk = self._df.read(self.RECORD_SIZE)
            rid = struct.unpack_from(self.RECORD_FMT, chunk, 0)[0]
            self._xf.write(struct.pack(self.IDX_FMT, rid, offset))
            offset += self.RECORD_SIZE
        self._xf.flush()

    def _load_index(self):
        self._by_id.clear()
        self._xf.seek(0, 2)
        total = self._xf.tell()
        self._xf.seek(0)
        while True:
            chunk = self._xf.read(self.IDX_SIZE)
            if len(chunk) < self.IDX_SIZE:
                break
            rid, off = struct.unpack(self.IDX_FMT, chunk)
            self._by_id[rid] = off

    @staticmethod
    def _pack_user(user):
        name_b = user.name.encode("utf-8")[:32]
        city_b = user.city.encode("utf-8")[:32]
        return struct.pack(FileDB.RECORD_FMT, user.id, name_b, user.age, city_b)

    @staticmethod
    def _unpack_user(chunk):
        rid, name_b, age, city_b = struct.unpack(FileDB.RECORD_FMT, chunk)
        return User(
            rid,
            name_b.rstrip(b"\x00").decode("utf-8", "replace"),
            age,
            city_b.rstrip(b"\x00").decode("utf-8", "replace"),
        )

    # ---- API псевдо-БД ----

    def add(self, record):
        rid = record.id
        if rid in self._by_id:
            raise ValueError(f"Duplicate id: {rid}")
        offset = self._df.seek(0, 2)
        self._df.write(self._pack_user(record))
        self._xf.seek(0, 2)
        self._xf.write(struct.pack(self.IDX_FMT, rid, offset))
        self._by_id[rid] = offset

    def bulk_add(self, users):
        """Пакетная запись — быстро и без лишних flush."""
        offset = self._df.seek(0, 2)
        data_buf = bytearray()
        idx_buf = bytearray()
        for u in users:
            if u.id in self._by_id:
                raise ValueError(f"Duplicate id: {u.id}")
            data_buf += self._pack_user(u)
            idx_buf += struct.pack(self.IDX_FMT, u.id, offset)
            self._by_id[u.id] = offset
            offset += self.RECORD_SIZE
        self._df.write(data_buf)
        self._xf.seek(0, 2)
        self._xf.write(idx_buf)

    def iter_all(self):
        """Ленивое чтение всех записей прямо с диска."""
        self._df.seek(0)
        while True:
            chunk = self._df.read(self.RECORD_SIZE)
            if len(chunk) < self.RECORD_SIZE:
                break
            yield self._unpack_user(chunk)

    def read_all(self):
        return list(self.iter_all())

    def get_by_id(self, id_):
        off = self._by_id.get(id_)
        if off is None:
            return None
        self._df.seek(off)
        chunk = self._df.read(self.RECORD_SIZE)
        if len(chunk) < self.RECORD_SIZE:
            return None
        return self._unpack_user(chunk)

    def search(self, predicate):
        for record in self.iter_all():
            if predicate(record):
                yield record

    def search_by(self, **conditions):
        for record in self.iter_all():
            match = True
            for field, value in conditions.items():
                if getattr(record, field) != value:
                    match = False
                    break
            if match:
                yield record

    def flush(self):
        if self._df:
            self._df.flush()
            os.fsync(self._df.fileno())
        if self._xf:
            self._xf.flush()
            os.fsync(self._xf.fileno())

    def close(self):
        try:
            self.flush()
        except Exception:
            pass
        if self._df:
            self._df.close()
            self._df = None
        if self._xf:
            self._xf.close()
            self._xf = None

    def destroy(self):
        """Удаляет файлы БД с накопителя."""
        self.close()
        for p in (self.data_path, self.index_path):
            if os.path.exists(p):
                os.remove(p)

    def storage_info(self):
        dsz = os.path.getsize(self.data_path) if os.path.exists(self.data_path) else 0
        xsz = os.path.getsize(self.index_path) if os.path.exists(self.index_path) else 0
        return dsz, xsz

    def __len__(self):
        return len(self._by_id)


# ---------- вспомогательные функции ввода ----------

def input_int(prompt, default=None):
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print("  Ожидалось целое число. Попробуйте снова.")


def print_records(records, limit=20):
    records = list(records)
    if not records:
        print("  Ничего не найдено.")
        return
    for r in records[:limit]:
        print("  ", r)
    if len(records) > limit:
        print(f"  ... и ещё {len(records) - limit} записей (показаны первые {limit}).")
    else:
        print(f"  Всего: {len(records)}.")


def human_size(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.2f} {unit}"
        n /= 1024


# ---------- действия меню ----------

def action_add(db):
    print("\n-- Добавление записи (на диск) --")
    id_ = input_int("  id: ")
    if id_ in db._by_id:
        print(f"  Ошибка: id={id_} уже существует.")
        return
    name = input("  name: ").strip() or f"user{id_}"
    age = input_int("  age: ", default=0)
    city = input("  city: ").strip() or "Unknown"
    db.add(User(id_, name, age, city))
    db.flush()
    print(f"  Записано на диск. Всего записей: {len(db)}")


def action_read_all(db):
    print("\n-- Чтение всех записей с диска --")
    if len(db) == 0:
        print("  База пуста.")
        return
    limit = input_int(
        f"  Сколько показать? (Enter = 20, всего {len(db)}): ", default=20
    )
    t0 = time.perf_counter()
    print_records(db.iter_all(), limit=limit)
    dt = time.perf_counter() - t0
    print(f"  Чтение заняло {dt:.3f} с.")


def action_get_by_id(db):
    print("\n-- Поиск по id (по индексу) --")
    id_ = input_int("  id: ")
    t0 = time.perf_counter()
    rec = db.get_by_id(id_)
    dt = time.perf_counter() - t0
    if rec is None:
        print(f"  Не найдено (за {dt*1000:.3f} мс).")
    else:
        print(f"  {rec} (за {dt*1000:.3f} мс).")


def action_search_by(db):
    print("\n-- Поиск по полям (сканирование файла) --")
    print("  Оставьте поле пустым, чтобы не фильтровать.")
    conditions = {}
    name = input("  name: ").strip()
    if name:
        conditions["name"] = name
    age_raw = input("  age: ").strip()
    if age_raw:
        try:
            conditions["age"] = int(age_raw)
        except ValueError:
            print("  age не число, пропускаем.")
    city = input("  city: ").strip()
    if city:
        conditions["city"] = city

    if not conditions:
        print("  Не задано ни одного условия.")
        return

    t0 = time.perf_counter()
    found = list(db.search_by(**conditions))
    dt = time.perf_counter() - t0
    print(f"  Условия: {conditions}. Найдено: {len(found)} за {dt:.4f} с.")
    print_records(found)


def action_search_predicate(db):
    print("\n-- Поиск по предикату (Python-выражение, скан файла) --")
    print("  Примеры:")
    print("    age > 30")
    print("    age == 42 and city == 'Omsk'")
    print("    name.startswith('user1')")
    print("    'so' in city.lower()")
    expr = input("  Условие: ").strip()
    if not expr:
        print("  Пустое условие.")
        return

    try:
        code = compile(expr, "<predicate>", "eval")
    except SyntaxError as e:
        print(f"  Синтаксическая ошибка: {e}")
        return

    def predicate(record):
        return bool(eval(code, {"__builtins__": {}}, {
            "id": record.id,
            "name": record.name,
            "age": record.age,
            "city": record.city,
        }))

    t0 = time.perf_counter()
    found = list(db.search(predicate))
    dt = time.perf_counter() - t0
    print(f"  Найдено: {len(found)} за {dt:.4f} с.")
    print_records(found)


def action_fill_demo(db):
    print("\n-- Генерация тестовых данных на диск --")
    n = input_int("  Сколько записей сгенерировать? (Enter = 1000000): ",
                  default=1_000_000)
    cities = ("Moscow", "Kazan", "Omsk", "Sochi", "Novosibirsk")
    start_id = max(db._by_id.keys(), default=-1) + 1

    batch_size = 50_000
    t0 = time.perf_counter()
    written = 0
    while written < n:
        chunk = min(batch_size, n - written)
        users = [
            User(
                id=start_id + written + i,
                name=f"user{start_id + written + i}",
                age=(start_id + written + i) % 100,
                city=cities[(start_id + written + i) % len(cities)],
            )
            for i in range(chunk)
        ]
        db.bulk_add(users)
        written += chunk
    db.flush()
    t1 = time.perf_counter()
    dsz, xsz = db.storage_info()
    print(f"  Добавлено {n} записей за {t1 - t0:.3f} с. "
          f"Всего: {len(db)}. "
          f"Файл данных: {human_size(dsz)}, индекс: {human_size(xsz)}.")


def action_benchmark(db):
    print("\n-- Бенчмарк (чтение с накопителя) --")
    if len(db) == 0:
        print("  База пуста — нечего тестировать.")
        return

    n = len(db)

    t0 = time.perf_counter()
    _ = db.read_all()
    t1 = time.perf_counter()
    print(f"  read_all({n}): {t1 - t0:.4f} с")

    target_id = max(db._by_id.keys())
    t0 = time.perf_counter()
    _ = db.get_by_id(target_id)
    t1 = time.perf_counter()
    print(f"  get_by_id({target_id}): {(t1 - t0) * 1e6:.2f} мкс")

    t0 = time.perf_counter()
    found = sum(1 for _ in db.search(lambda u: u.age == 42 and u.city == "Omsk"))
    t1 = time.perf_counter()
    print(f"  search(predicate) по всему файлу: найдено {found} за {t1 - t0:.4f} с")

    t0 = time.perf_counter()
    found = sum(1 for _ in db.search_by(age=42, city="Omsk"))
    t1 = time.perf_counter()
    print(f"  search_by(age=42, city=Omsk): найдено {found} за {t1 - t0:.4f} с")


def action_info(db):
    dsz, xsz = db.storage_info()
    print("\n-- Информация о хранилище --")
    print(f"  Файл данных : {db.data_path} ({human_size(dsz)})")
    print(f"  Файл индекса: {db.index_path} ({human_size(xsz)})")
    print(f"  Записей     : {len(db)}")
    print(f"  Размер одной записи: {FileDB.RECORD_SIZE} байт")


def action_destroy(db):
    print("\n-- Удаление файлов БД с накопителя --")
    ans = input("  Вы уверены? (y/N): ").strip().lower()
    if ans != "y":
        print("  Отменено.")
        return
    db.destroy()
    db._open()  # создаём заново пустую
    print("  База очищена.")


# ---------- главное меню ----------

MENU = """
============ Pseudo DB on Disk (SSD/HDD) ============
 Файл данных : {data_path}
 Записей     : {count}
----------------------------------------------------
 1. Добавить запись
 2. Прочитать все записи с диска
 3. Найти по id (по индексу)
 4. Найти по полям (name/age/city)
 5. Найти по предикату (произвольное условие)
 6. Сгенерировать 1 000 000 тестовых записей на диск
 7. Бенчмарк
 8. Информация о хранилище
 9. Удалить файлы БД
 0. Выход
====================================================
"""


def main():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.db")
    db = FileDB(db_path)

    actions = {
        "1": action_add,
        "2": action_read_all,
        "3": action_get_by_id,
        "4": action_search_by,
        "5": action_search_predicate,
        "6": action_fill_demo,
        "7": action_benchmark,
        "8": action_info,
        "9": action_destroy,
    }

    try:
        while True:
            print(MENU.format(count=len(db), data_path=db.data_path))
            choice = input("Выберите пункт: ").strip()

            if choice == "0":
                print("Выход.")
                break

            action = actions.get(choice)
            if action is None:
                print("  Неизвестный пункт меню.")
                continue

            try:
                action(db)
            except KeyboardInterrupt:
                print("\n  Прервано пользователем.")
            except Exception as e:
                print(f"  Ошибка: {type(e).__name__}: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()