#!/usr/bin/env python3
"""
bench.py — сравнение производительности трёх псевдо-БД:
  1) InMemoryDB   (семинар 5) — список в оперативной памяти
  2) FileDB       (семинар 6) — бинарный файл + индекс на накопителе
  3) PgDB         (PostgreSQL) — настоящая СУБД

Замеры на N = 1_000 / 10_000 / 100_000 записей.
Операции: массовая вставка, полное чтение, точечный поиск по id,
поиск по предикату (age == 42 and city == 'Omsk').

Выход:
  results.json         — «сырые» числа
  bench_all.png        — общий график 2x2 (matplotlib)
  bench_<метрика>.png  — отдельные графики по каждой операции
"""

import getpass
import json
import os
import struct
import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


# ======================= НАСТРОЙКИ PostgreSQL =======================
# Заполните здесь — это самый надёжный способ.
# Всё, что оставите как None, будет взято из переменных окружения,
# а если и там пусто — из libpq-дефолтов.

PG_CONFIG = {
    "host":     "localhost",      # напр. "localhost" или "127.0.0.1"
    "port":     5432,      # напр. 5432
    "user":     "postgres",      # напр. "postgres"
    "password": "postgres",      # <-- ВПИШИТЕ СЮДА ПАРОЛЬ, напр. "postgres"
    "dbname":   "postgres",      # напр. "postgres"
}

# Если True — спросит пароль в консоли, когда он не задан нигде.
ASK_PASSWORD_INTERACTIVELY = True
# =====================================================================


CITIES = ("Moscow", "Kazan", "Omsk", "Sochi", "Novosibirsk")
SIZES = (1_000, 10_000, 100_000)
POINT_LOOKUPS = 1000     # сколько точечных поисков усредняем


# ======================= модель =======================

class User:
    __slots__ = ("id", "name", "age", "city")

    def __init__(self, id, name, age, city):
        self.id = id
        self.name = name
        self.age = age
        self.city = city

    def __repr__(self):
        return (f"User(id={self.id}, name={self.name!r}, "
                f"age={self.age}, city={self.city!r})")


def gen_users(n, start=0):
    return [
        User(start + i, f"user{start + i}",
             (start + i) % 100, CITIES[(start + i) % len(CITIES)])
        for i in range(n)
    ]


# ======================= 1) InMemoryDB =======================

class InMemoryDB:
    """Псевдо-БД целиком в оперативной памяти (семинар 5)."""

    def __init__(self):
        self._records = []
        self._by_id = {}

    def add(self, r):
        if r.id in self._by_id:
            raise ValueError(r.id)
        self._records.append(r)
        self._by_id[r.id] = r

    def read_all(self):
        return list(self._records)

    def iter_all(self):
        return iter(self._records)

    def get_by_id(self, i):
        return self._by_id.get(i)

    def search(self, predicate):
        for r in self._records:
            if predicate(r):
                yield r

    def __len__(self):
        return len(self._records)


# ======================= 2) FileDB (на диске) =======================

class FileDB:
    """Псевдо-БД на накопителе (SSD/HDD), семинар 6."""

    RECORD_FMT = "<q32sq32s"
    RECORD_SIZE = struct.calcsize(RECORD_FMT)   # 80 байт
    IDX_FMT = "<qq"
    IDX_SIZE = struct.calcsize(IDX_FMT)         # 16 байт

    def __init__(self, data_path):
        self.data_path = data_path
        self.index_path = data_path + ".idx"
        for p in (self.data_path, self.index_path):
            if os.path.exists(p):
                os.remove(p)
        self._df = open(self.data_path, "w+b")
        self._xf = open(self.index_path, "w+b")
        self._by_id = {}

    @staticmethod
    def _pack(u):
        return struct.pack(FileDB.RECORD_FMT, u.id,
                           u.name.encode("utf-8")[:32], u.age,
                           u.city.encode("utf-8")[:32])

    @staticmethod
    def _unpack(chunk):
        rid, nb, age, cb = struct.unpack(FileDB.RECORD_FMT, chunk)
        return User(rid,
                    nb.rstrip(b"\x00").decode("utf-8", "replace"),
                    age,
                    cb.rstrip(b"\x00").decode("utf-8", "replace"))

    def bulk_add(self, users):
        off = self._df.seek(0, 2)
        dbuf = bytearray()
        ibuf = bytearray()
        for u in users:
            if u.id in self._by_id:
                raise ValueError(u.id)
            dbuf += self._pack(u)
            ibuf += struct.pack(self.IDX_FMT, u.id, off)
            self._by_id[u.id] = off
            off += self.RECORD_SIZE
        self._df.write(dbuf)
        self._xf.seek(0, 2)
        self._xf.write(ibuf)
        self._df.flush()
        self._xf.flush()

    def iter_all(self):
        self._df.seek(0)
        while True:
            chunk = self._df.read(self.RECORD_SIZE)
            if len(chunk) < self.RECORD_SIZE:
                break
            yield self._unpack(chunk)

    def read_all(self):
        return list(self.iter_all())

    def get_by_id(self, i):
        off = self._by_id.get(i)
        if off is None:
            return None
        self._df.seek(off)
        chunk = self._df.read(self.RECORD_SIZE)
        return self._unpack(chunk) if len(chunk) == self.RECORD_SIZE else None

    def search(self, predicate):
        for r in self.iter_all():
            if predicate(r):
                yield r

    def close(self):
        self._df.close()
        self._xf.close()

    def __len__(self):
        return len(self._by_id)


# ======================= 3) PostgreSQL =======================

class PgDB:
    """Обёртка над PostgreSQL для бенчмарка."""

    def __init__(self, params, table="bench_users"):
        import psycopg2
        self.conn = psycopg2.connect(**params)
        self.conn.autocommit = False
        self.table = table
        with self.conn.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {table}")
            cur.execute(f"""
                CREATE TABLE {table} (
                    id   BIGINT PRIMARY KEY,
                    name VARCHAR(64) NOT NULL,
                    age  INT NOT NULL,
                    city VARCHAR(64) NOT NULL
                )
            """)
        self.conn.commit()

    def bulk_add(self, users):
        from psycopg2.extras import execute_values
        with self.conn.cursor() as cur:
            execute_values(
                cur,
                f"INSERT INTO {self.table} (id, name, age, city) VALUES %s",
                [(u.id, u.name, u.age, u.city) for u in users],
                page_size=10_000,
            )
        self.conn.commit()

    def read_all(self):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT id, name, age, city FROM {self.table}")
            return [User(*row) for row in cur.fetchall()]

    def get_by_id(self, i):
        with self.conn.cursor() as cur:
            cur.execute(
                f"SELECT id, name, age, city FROM {self.table} WHERE id = %s",
                (i,),
            )
            row = cur.fetchone()
            return User(*row) if row else None

    def search_predicate_bench(self):
        """Эмулирует предикат age == 42 AND city == 'Omsk' средствами SQL."""
        with self.conn.cursor(name="bench_cur") as cur:
            cur.itersize = 10_000
            cur.execute(
                f"SELECT id, name, age, city FROM {self.table} "
                f"WHERE age = 42 AND city = 'Omsk'"
            )
            return [User(*row) for row in cur]

    def close(self):
        self.conn.close()


# ======================= параметры и проверка PostgreSQL =======================

def try_pg_params():
    """
    Собирает параметры подключения в порядке приоритета:
      1) PG_CONFIG из файла скрипта
      2) переменные окружения PGHOST/PGPORT/PGUSER/PGPASSWORD/PGDATABASE
      3) libpq-дефолты
    Плюс (опционально) интерактивный ввод пароля, если он так и не задан.
    """
    params = {}
    env_map = (("PGHOST", "host"), ("PGPORT", "port"),
               ("PGUSER", "user"), ("PGPASSWORD", "password"),
               ("PGDATABASE", "dbname"))

    # 1) из файла
    for k, v in PG_CONFIG.items():
        if v is not None and v != "":
            params[k] = v

    # 2) из окружения (что не задано в файле)
    for env, key in env_map:
        if key in params:
            continue
        v = os.environ.get(env)
        if v:
            params[key] = v

    # приведём порт к int, если он пришёл строкой
    if "port" in params:
        try:
            params["port"] = int(params["port"])
        except (TypeError, ValueError):
            pass

    # 3) интерактивно спросим пароль
    if "password" not in params and ASK_PASSWORD_INTERACTIVELY:
        try:
            pwd = getpass.getpass(
                "Пароль PostgreSQL (Enter — оставить пустым и попробовать "
                "libpq-дефолт): "
            )
            if pwd:
                params["password"] = pwd
        except (EOFError, KeyboardInterrupt):
            pass

    return params


def check_pg(pg_params):
    """Возвращает True, если PostgreSQL доступен. Печатает понятную диагностику."""
    try:
        import psycopg2
    except ImportError:
        print("psycopg2 не установлен. Установите: pip install psycopg2-binary")
        return False

    # не показываем пароль в логе
    safe = {k: ("***" if k == "password" else v)
            for k, v in (pg_params or {}).items()}

    try:
        conn = psycopg2.connect(**pg_params)
        with conn.cursor() as cur:
            cur.execute("SELECT version()")
            ver = cur.fetchone()[0]
        conn.close()
        print(f"PostgreSQL доступен. params={safe or 'libpq defaults'}")
        print(f"  server: {ver.split(',')[0]}")
        return True
    except Exception as e:
        print("PostgreSQL НЕДОСТУПЕН.")
        print(f"  params: {safe or 'libpq defaults'}")
        print(f"  ошибка: {type(e).__name__}: {e}")
        print()
        print("  Подсказки:")
        print("  • Пароль можно вписать прямо в PG_CONFIG в начале файла.")
        print("  • Либо задать переменные окружения:")
        print("      Windows (cmd):        set PGPASSWORD=ваш_пароль")
        print("      Windows (PowerShell): $env:PGPASSWORD='ваш_пароль'")
        print("      Linux/macOS:          export PGPASSWORD=ваш_пароль")
        print("  • Проверьте, что сервер запущен и принимает соединения:")
        print("      pg_isready -h <host> -p <port>")
        print("  • Пользователь/БД существуют? Проверьте через psql:")
        print("      psql -h <host> -U <user> -d <dbname>")
        return False


# ======================= запуск бенчмарка =======================

def measure(fn):
    t0 = time.perf_counter()
    result = fn()
    return time.perf_counter() - t0, result


def bench_one_size(n, pg_params=None):
    print(f"\n=== N = {n:,} ===")
    users = gen_users(n)
    res = {"n": n}

    # ---------- InMemoryDB ----------
    print("  InMemoryDB ...", end=" ", flush=True)
    db = InMemoryDB()
    dt, _ = measure(lambda: [db.add(u) for u in users])
    res["memory_insert"] = dt

    dt, _ = measure(db.read_all)
    res["memory_read_all"] = dt

    def point_mem():
        for _ in range(POINT_LOOKUPS):
            db.get_by_id(n // 2)
    dt, _ = measure(point_mem)
    res["memory_get_by_id"] = dt / POINT_LOOKUPS

    dt, _ = measure(lambda: list(db.search(
        lambda u: u.age == 42 and u.city == "Omsk")))
    res["memory_search"] = dt
    del db
    print("ok")

    # ---------- FileDB ----------
    print("  FileDB     ...", end=" ", flush=True)
    db = FileDB("bench_file.db")
    dt, _ = measure(lambda: db.bulk_add(users))
    res["file_insert"] = dt

    dt, _ = measure(db.read_all)
    res["file_read_all"] = dt

    def point_file():
        for _ in range(POINT_LOOKUPS):
            db.get_by_id(n // 2)
    dt, _ = measure(point_file)
    res["file_get_by_id"] = dt / POINT_LOOKUPS

    dt, _ = measure(lambda: list(db.search(
        lambda u: u.age == 42 and u.city == "Omsk")))
    res["file_search"] = dt
    db.close()
    for p in ("bench_file.db", "bench_file.db.idx"):
        if os.path.exists(p):
            os.remove(p)
    print("ok")

    # ---------- PostgreSQL ----------
    if pg_params is not None:
        print("  PostgreSQL ...", end=" ", flush=True)
        try:
            db = PgDB(pg_params)
            dt, _ = measure(lambda: db.bulk_add(users))
            res["pg_insert"] = dt

            dt, _ = measure(db.read_all)
            res["pg_read_all"] = dt

            def point_pg():
                for _ in range(POINT_LOOKUPS):
                    db.get_by_id(n // 2)
            dt, _ = measure(point_pg)
            res["pg_get_by_id"] = dt / POINT_LOOKUPS

            dt, _ = measure(db.search_predicate_bench)
            res["pg_search"] = dt
            db.close()
            print("ok")
        except Exception as e:
            print(f"пропущен ({type(e).__name__}: {e})")
            for k in ("pg_insert", "pg_read_all",
                      "pg_get_by_id", "pg_search"):
                res[k] = None
    else:
        for k in ("pg_insert", "pg_read_all",
                  "pg_get_by_id", "pg_search"):
            res[k] = None

    for k, v in res.items():
        if k == "n":
            continue
        if v is None:
            print(f"    {k:18s}: N/A")
        elif v < 1e-3:
            print(f"    {k:18s}: {v * 1e6:>10.2f} мкс")
        else:
            print(f"    {k:18s}: {v:>10.6f} с")

    return res


# ======================= визуализация (matplotlib) =======================

DB_STYLE = [
    ("memory", "InMemoryDB", "#4c78a8"),
    ("file",   "FileDB",     "#f58518"),
    ("pg",     "PostgreSQL", "#54a24b"),
]

METRICS = [
    ("insert",    "Массовая вставка N записей",             False),
    ("read_all",  "Полное чтение всех записей",              True),
    ("get_by_id", "Точечный поиск по id (среднее ×1000)",    True),
    ("search",    "Поиск age=42 AND city='Omsk'",            True),
]


def _safe(v):
    """matplotlib не любит 0 и None на log-оси."""
    if v is None:
        return np.nan
    return max(v, 1e-9)


def _fmt(v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    if v < 1e-3:
        return f"{v * 1e6:.1f} мкс"
    if v < 1:
        return f"{v * 1e3:.2f} мс"
    return f"{v:.3f} с"


def plot_results(results, combined_path="bench_all.png"):
    sizes = [r["n"] for r in results]
    x = np.arange(len(sizes))
    width = 0.26

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    axes = axes.ravel()

    for ax, (key, title, log_scale) in zip(axes, METRICS):
        for i, (db_id, db_label, color) in enumerate(DB_STYLE):
            ys = [_safe(r.get(f"{db_id}_{key}")) for r in results]
            bars = ax.bar(x + (i - 1) * width, ys, width,
                          label=db_label, color=color, edgecolor="black",
                          linewidth=0.4)
            for b, y in zip(bars, ys):
                if np.isnan(y):
                    continue
                ax.annotate(_fmt(y),
                            xy=(b.get_x() + b.get_width() / 2, y),
                            xytext=(0, 3), textcoords="offset points",
                            ha="center", va="bottom", fontsize=7.5)

        ax.set_title(title)
        ax.set_xlabel("Количество записей, N")
        ax.set_ylabel("Время, с")
        ax.set_xticks(x)
        ax.set_xticklabels([f"{s:,}".replace(",", " ") for s in sizes])
        if log_scale:
            ax.set_yscale("log")
        ax.grid(True, which="both", axis="y", alpha=0.3)
        ax.legend(fontsize=9)

    fig.suptitle("Сравнение псевдо-БД и PostgreSQL", fontsize=14)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(combined_path, dpi=130)
    print(f"Сохранён общий график: {os.path.abspath(combined_path)}")

    # отдельные PNG на каждую операцию
    for key, title, log_scale in METRICS:
        fig2, ax = plt.subplots(figsize=(8, 5))
        for i, (db_id, db_label, color) in enumerate(DB_STYLE):
            ys = [_safe(r.get(f"{db_id}_{key}")) for r in results]
            bars = ax.bar(x + (i - 1) * width, ys, width,
                          label=db_label, color=color, edgecolor="black",
                          linewidth=0.4)
            for b, y in zip(bars, ys):
                if np.isnan(y):
                    continue
                ax.annotate(_fmt(y),
                            xy=(b.get_x() + b.get_width() / 2, y),
                            xytext=(0, 3), textcoords="offset points",
                            ha="center", va="bottom", fontsize=8)

        ax.set_title(title)
        ax.set_xlabel("Количество записей, N")
        ax.set_ylabel("Время, с")
        ax.set_xticks(x)
        ax.set_xticklabels([f"{s:,}".replace(",", " ") for s in sizes])
        if log_scale:
            ax.set_yscale("log")
        ax.grid(True, which="both", axis="y", alpha=0.3)
        ax.legend()
        fig2.tight_layout()
        out = f"bench_{key}.png"
        fig2.savefig(out, dpi=130)
        print(f"Сохранён график: {os.path.abspath(out)}")
        plt.close(fig2)

    plt.show()


def print_summary_table(results):
    print("\n===================== ИТОГОВАЯ ТАБЛИЦА =====================")
    header = f"{'Операция':<28}"
    for db_id, db_label, _ in DB_STYLE:
        for n in SIZES:
            header += f" {db_label[:6]:>10} N={n:<6}"
    print(header)
    print("-" * len(header))
    for key, title, _ in METRICS:
        line = f"{title[:27]:<28}"
        for db_id, _, _ in DB_STYLE:
            for n in SIZES:
                row = next((r for r in results if r["n"] == n), None)
                v = row.get(f"{db_id}_{key}") if row else None
                line += f" {_fmt(v):>16}"
        print(line)


# ======================= main =======================

def main():
    pg_params = try_pg_params()
    pg_ok = check_pg(pg_params)

    results = []
    for n in SIZES:
        results.append(bench_one_size(n, pg_params if pg_ok else None))

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\nРезультаты: results.json")

    print_summary_table(results)
    plot_results(results, "bench_all.png")


if __name__ == "__main__":
    main()