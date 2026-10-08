import time


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


class InMemoryDB:
    def __init__(self):
        self._records = []
        self._by_id = {}

    def add(self, record):
        rid = record.id
        if rid in self._by_id:
            raise ValueError(f"Duplicate id: {rid}")
        self._records.append(record)
        self._by_id[rid] = record

    def read_all(self):
        return list(self._records)

    def iter_all(self):
        return iter(self._records)

    def get_by_id(self, id_):
        return self._by_id.get(id_)

    def search(self, predicate):
        for record in self._records:
            if predicate(record):
                yield record

    def search_by(self, **conditions):
        for record in self._records:
            match = True
            for field, value in conditions.items():
                if getattr(record, field) != value:
                    match = False
                    break
            if match:
                yield record

    def __len__(self):
        return len(self._records)


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
    shown = records[:limit]
    for r in shown:
        print("  ", r)
    if len(records) > limit:
        print(f"  ... и ещё {len(records) - limit} записей (показаны первые {limit}).")
    else:
        print(f"  Всего: {len(records)}.")


# ---------- действия меню ----------

def action_add(db):
    print("\n-- Добавление записи --")
    id_ = input_int("  id: ")
    if id_ in db._by_id:
        print(f"  Ошибка: id={id_} уже существует.")
        return
    name = input("  name: ").strip() or f"user{id_}"
    age = input_int("  age: ", default=0)
    city = input("  city: ").strip() or "Unknown"
    db.add(User(id_, name, age, city))
    print(f"  Добавлено. Всего записей: {len(db)}")


def action_read_all(db):
    print("\n-- Все записи --")
    if len(db) == 0:
        print("  База пуста.")
        return
    limit = input_int(
        f"  Сколько показать? (Enter = 20, всего {len(db)}): ", default=20
    )
    print_records(db.iter_all(), limit=limit)


def action_get_by_id(db):
    print("\n-- Поиск по id --")
    id_ = input_int("  id: ")
    t0 = time.perf_counter()
    rec = db.get_by_id(id_)
    dt = time.perf_counter() - t0
    if rec is None:
        print(f"  Не найдено (за {dt*1000:.3f} мс).")
    else:
        print(f"  {rec} (за {dt*1000:.3f} мс).")


def action_search_by(db):
    print("\n-- Поиск по полям --")
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
    print("\n-- Поиск по предикату (Python-выражение) --")
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
    print("\n-- Заполнение тестовыми данными --")
    n = input_int("  Сколько записей сгенерировать? (Enter = 1000000): ",
                  default=1_000_000)
    cities = ("Moscow", "Kazan", "Omsk", "Sochi", "Novosibirsk")
    start_id = max(db._by_id.keys(), default=-1) + 1
    t0 = time.perf_counter()
    for i in range(start_id, start_id + n):
        db.add(User(
            id=i,
            name=f"user{i}",
            age=i % 100,
            city=cities[i % len(cities)],
        ))
    t1 = time.perf_counter()
    print(f"  Добавлено {n} записей за {t1 - t0:.3f} с. Всего: {len(db)}")


def action_benchmark(db):
    print("\n-- Бенчмарк --")
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
    print(f"  search(predicate): найдено {found} за {t1 - t0:.4f} с")


# ---------- главное меню ----------

MENU = """
================= In-Memory DB =================
 Записей в базе: {count}
------------------------------------------------
 1. Добавить запись
 2. Показать все записи
 3. Найти по id
 4. Найти по полям (name/age/city)
 5. Найти по предикату (произвольное условие)
 6. Заполнить тестовыми данными (1 000 000 по умолчанию)
 7. Бенчмарк
 0. Выход
================================================
"""


def main():
    db = InMemoryDB()
    actions = {
        "1": action_add,
        "2": action_read_all,
        "3": action_get_by_id,
        "4": action_search_by,
        "5": action_search_predicate,
        "6": action_fill_demo,
        "7": action_benchmark,
    }

    while True:
        print(MENU.format(count=len(db)))
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


if __name__ == "__main__":
    main()