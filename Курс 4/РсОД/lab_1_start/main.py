
import json
import os
import socket
import subprocess
import sys
import threading
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
ITEM_COLUMNS = ["id", "name", "category", "value", "updated_at", "active"]
STATISTICS_PATH = PROCESSED_DIR / "course_4_report.csv"
STATISTICS_MARKDOWN_PATH = PROCESSED_DIR / "course_4_report.md"


def select_csv_separator():
    separators = {"1": (",", "запятая"), "2": (";", "точка с запятой"), "3": ("\t", "табуляция")}
    while True:
        print("Выберите разделитель CSV-файла:")
        print("1. Запятая (,)")
        print("2. Точка с запятой (;)")
        print("3. Табуляция")
        choice = input("Введите номер разделителя: ").strip()
        if choice in separators:
            separator, name = separators[choice]
            print(f"Выбран разделитель: {name}")
            return separator
        print("Неверный выбор. Введите 1, 2 или 3.")


def read_items_csv(path, separator=","):
    """Read CSV with the separator selected by the user."""
    return pd.read_csv(path, sep=separator)


def read_items_json(path):
    """Parse JSON structure with the standard library before creating a DataFrame."""
    with path.open(encoding="utf-8") as file:
        records = json.load(file)
    if not isinstance(records, list) or not all(isinstance(record, dict) for record in records):
        raise ValueError("JSON must contain a list of objects")
    return pd.DataFrame(records)


def read_items_xml(path):
    """Parse XML rows with xml.etree.ElementTree."""
    root = ET.parse(path).getroot()
    records = [{child.tag: child.text for child in row} for row in root.findall("row")]
    return pd.DataFrame(records)


def normalize_items(df):
    """Convert an item table to the common schema and remove exact duplicates."""
    result = df.copy()
    for column in ITEM_COLUMNS:
        if column not in result:
            result[column] = pd.NA
    result = result[ITEM_COLUMNS]

    result["id"] = pd.to_numeric(result["id"], errors="coerce").astype("Int64")
    result["name"] = result["name"].astype("string").str.strip()
    result["value"] = pd.to_numeric(result["value"], errors="coerce")
    result["updated_at"] = pd.to_datetime(
        result["updated_at"], errors="coerce", format="mixed", dayfirst=False
    )

    category = result["category"].astype("string").str.strip().str.casefold()
    category_aliases = {
        "category a": "Category A",
        "cat a": "Category A",
        "category b": "Category B",
        "cat b": "Category B",
        "category c": "Category C",
        "cat c": "Category C",
    }
    result["category"] = category.map(category_aliases).fillna(
        category.str.replace(r"\s+", " ", regex=True).str.title()
    )

    active_values = result["active"].astype("string").str.strip().str.casefold()
    result["active"] = active_values.map(
        {"true": True, "false": False, "1": True, "0": False, "yes": True, "no": False}
    ).astype("boolean")
    return result.drop_duplicates(ignore_index=True)


def print_source_report(name, df):
    duplicate_ids = int(df.loc[df["id"].duplicated(keep=False), "id"].nunique())
    duplicate_rows = int(df["id"].duplicated(keep=False).sum())
    print(f"\n{name}")
    print(f"Количество записей: {len(df)}")
    print(f"Столбцы: {list(df.columns)}")
    print(f"Типы данных:\n{df.dtypes.to_string()}")
    print(f"Пропущенные значения:\n{df.isna().sum().to_string()}")
    print(f"Количество повторяющихся id: {duplicate_ids} (записей с ними: {duplicate_rows})")


def save_as_xml(df, path):
    export = df.copy()
    export["updated_at"] = export["updated_at"].dt.strftime("%Y-%m-%d %H:%M:%S")
    export.to_xml(path, index=False, root_name="data", row_name="row")


def process_items(csv_separator):
    sources = {
        "CSV": read_items_csv(RAW_DIR / "items.csv", csv_separator),
        "JSON": read_items_json(RAW_DIR / "items.json"),
        "XML": read_items_xml(RAW_DIR / "items.xml"),
    }
    for name, source in sources.items():
        print_source_report(name, source)

    normalized = []
    for priority, (name, source) in enumerate(sources.items()):
        current = normalize_items(source)
        current["_source_priority"] = priority
        normalized.append(current)

    combined = pd.concat(normalized, ignore_index=True)
    combined = combined.drop_duplicates(subset=ITEM_COLUMNS, ignore_index=True)
    combined = combined.sort_values(
        ["id", "updated_at", "_source_priority"],
        ascending=[True, False, True],
        na_position="last",
    )
    result = combined.drop_duplicates(subset="id", keep="first").sort_values("id")
    result = result[ITEM_COLUMNS].reset_index(drop=True)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    result.to_csv(PROCESSED_DIR / "items_normalized.csv", index=False)
    result.to_json(PROCESSED_DIR / "items_normalized.json", orient="records", force_ascii=False, date_format="iso")
    save_as_xml(result, PROCESSED_DIR / "items_normalized.xml")

    print("\nКонфликты id разрешены правилом: выбирается запись с наиболее поздним updated_at;")
    print("при одинаковой дате приоритет имеют CSV, затем JSON, затем XML.")
    print(f"\nНормализовано и сохранено записей: {len(result)}")
    print(f"Результаты: {PROCESSED_DIR}")
    return result


def course_1():
    started = time.perf_counter()
    csv_separator = select_csv_separator()
    result = process_items(csv_separator)
    save_statistics(
        {
            "Способ": "CSV/XML/JSON",
            "Количество записей": len(result),
            "Уникальных id": result["id"].nunique(),
            "Время, с": round(time.perf_counter() - started, 4),
            "Есть ошибки": "Нет",
        }
    )
    return result


def save_statistics(statistic):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    statistics = []
    if STATISTICS_PATH.exists():
        statistics = pd.read_csv(STATISTICS_PATH).to_dict(orient="records")
        statistics = [
            row
            for row in statistics
            if row.get("Способ") not in {statistic["Способ"], "CSV/XMSL/JSON"}
        ]
    statistics.append(statistic)
    report = pd.DataFrame(statistics)
    report.to_csv(STATISTICS_PATH, index=False)

    markdown_rows = [
        "| Способ | Количество записей | Уникальных id | Время, с | Есть ошибки |",
        "|---|---:|---:|---:|---|",
    ]
    for row in statistics:
        markdown_rows.append(
            f"| {row['Способ']} | {row['Количество записей']} | "
            f"{row['Уникальных id']} | {row['Время, с']} | {row['Есть ошибки']} |"
        )
    markdown_rows.extend(
        [
            "",
            "### Вывод",
            "",
            "Если существует официальный API, для структурированных данных предпочтительнее "
            "использовать его, а не браузерную автоматизацию. API возвращает данные в "
            "машиночитаемом формате, имеет стабильный контракт и позволяет обращаться к "
            "нужным ресурсам напрямую. Это обычно быстрее, проще для обработки и надежнее "
            "при обновлении верстки. Selenium зависит от DOM, JavaScript, браузера и "
            "явных ожиданий, поэтому он нужен прежде всего для сценариев, где данные "
            "доступны только через пользовательский интерфейс.",
        ]
    )
    STATISTICS_MARKDOWN_PATH.write_text("\n".join(markdown_rows), encoding="utf-8")


def _response_body(response):
    """Parse JSON when possible without confusing parsing with HTTP success."""
    try:
        return response.json()
    except ValueError:
        return response.text


def _save_request_result(results, method, url, request_data, response, started):
    result = {
        "method": method,
        "url": url,
        "params_or_body": request_data,
        "status_code": response.status_code,
        "content_type": response.headers.get("content-type"),
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
        "response": _response_body(response),
    }
    results.append(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def _save_request_error(results, method, url, request_data, error, started, response=None):
    result = {
        "method": method,
        "url": url,
        "params_or_body": request_data,
        "status_code": response.status_code if response is not None else None,
        "content_type": response.headers.get("content-type") if response is not None else None,
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
        "response": _response_body(response) if response is not None else None,
        "error_type": type(error).__name__,
        "error": str(error),
    }
    results.append(result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def course_2():
    """Run and document a complete CRUD scenario against the local backend."""
    host = "127.0.0.1"
    port = 8000
    base_url = f"http://{host}:{port}"
    items_url = f"{base_url}/api/items"
    results = []
    backend_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.main:app",
            "--host",
            host,
            "--port",
            str(port),
        ],
        cwd=BASE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )

    try:
        for _ in range(20):
            if backend_process.poll() is not None:
                raise RuntimeError("Локальный backend завершился до запуска")
            try:
                response = requests.get(items_url, timeout=10)
                response.raise_for_status()
                break
            except requests.RequestException:
                time.sleep(0.25)
        else:
            raise RuntimeError("Не удалось дождаться запуска локального backend")

        post_body = {
            "name": "Course 2 item",
            "category": "Category A",
            "value": 123.45,
            "updated_at": "2026-09-08 12:00:00",
            "active": True,
        }
        started = time.perf_counter()
        response = requests.post(items_url, json=post_body, timeout=10)
        response.raise_for_status()
        _save_request_result(results, "POST", items_url, post_body, response, started)
        item_id = response.json()["id"]
        item_url = f"{items_url}/{item_id}"

        put_body = {
            "name": "Course 2 item replaced",
            "category": "Category B",
            "value": 456.78,
            "updated_at": "2026-09-08 13:00:00",
            "active": False,
        }
        started = time.perf_counter()
        response = requests.put(item_url, json=put_body, timeout=10)
        response.raise_for_status()
        _save_request_result(results, "PUT", item_url, put_body, response, started)

        patch_body = {"name": "Course 2 item patched"}
        started = time.perf_counter()
        response = requests.patch(item_url, json=patch_body, timeout=10)
        response.raise_for_status()
        _save_request_result(results, "PATCH", item_url, patch_body, response, started)

        started = time.perf_counter()
        response = requests.get(item_url, timeout=10)
        response.raise_for_status()
        _save_request_result(results, "GET", item_url, None, response, started)

        started = time.perf_counter()
        response = requests.delete(item_url, timeout=10)
        response.raise_for_status()
        _save_request_result(results, "DELETE", item_url, None, response, started)

        started = time.perf_counter()
        response = requests.get(item_url, timeout=10)
        try:
            response.raise_for_status()
        except requests.RequestException as error:
            if response.status_code != 404:
                raise
            print("Финальный GET подтвердил удаление ресурса: HTTP 404")
            _save_request_error(results, "GET", item_url, None, error, started, response)

        closed_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        closed_socket.bind((host, 0))
        connection_error_port = closed_socket.getsockname()[1]
        closed_socket.close()
        connection_error_url = f"http://{host}:{connection_error_port}/api/items"
        started = time.perf_counter()
        response = None
        try:
            response = requests.get(connection_error_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as error:
            _save_request_error(results, "GET", connection_error_url, None, error, started, response)

        timeout_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        timeout_socket.bind((host, 0))
        timeout_socket.listen(1)
        timeout_port = timeout_socket.getsockname()[1]

        def hold_connection():
            try:
                connection, _ = timeout_socket.accept()
                time.sleep(1)
                connection.close()
            except OSError:
                pass

        timeout_thread = threading.Thread(target=hold_connection, daemon=True)
        timeout_thread.start()
        timeout_url = f"http://{host}:{timeout_port}/api/items"
        started = time.perf_counter()
        response = None
        try:
            response = requests.get(timeout_url, timeout=0.05)
            response.raise_for_status()
        except requests.RequestException as error:
            _save_request_error(results, "GET", timeout_url, None, error, started, response)
        finally:
            timeout_socket.close()
            timeout_thread.join(timeout=2)
    finally:
        output_path = PROCESSED_DIR / "course_2_requests.json"
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()
        print(f"Результаты запросов сохранены: {output_path}")
    items_path = PROCESSED_DIR / "items_normalized.json"
    items_count = len(json.loads(items_path.read_text(encoding="utf-8"))) if items_path.exists() else 0
    save_statistics(
        {
            "Способ": "REST API",
            "Количество записей": items_count,
            "Уникальных id": items_count,
            "Время, с": round(sum(item["elapsed_ms"] for item in results) / 1000, 4),
            "Есть ошибки": "Да" if any("error" in item for item in results) else "Нет",
        }
    )
    return results

def course_3():
    """Load the dynamic page with Selenium and save its filtered table."""
    started = time.perf_counter()
    host = "127.0.0.1"
    port = 8000
    base_url = f"http://{host}:{port}"
    backend_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.main:app",
            "--host",
            host,
            "--port",
            str(port),
        ],
        cwd=BASE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    driver = None

    try:
        for _ in range(20):
            if backend_process.poll() is not None:
                raise RuntimeError("Локальный backend завершился до запуска")
            try:
                response = requests.get(f"{base_url}/dynamic", timeout=10)
                response.raise_for_status()
                break
            except requests.RequestException:
                time.sleep(0.25)
        else:
            raise RuntimeError("Не удалось дождаться запуска локального backend")

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(10)
        driver.set_script_timeout(10)
        wait = WebDriverWait(driver, 10)
        driver.get(f"{base_url}/dynamic")

        load_button = wait.until(
            EC.element_to_be_clickable((By.ID, "load-button"))
        )
        load_button.click()
        wait.until(
            lambda browser: browser.find_elements(By.CSS_SELECTOR, "#items-body tr")
        )

        category_filter = wait.until(
            EC.element_to_be_clickable((By.ID, "category-filter"))
        )
        Select(category_filter).select_by_visible_text("Category B")

        def filtered_rows(browser):
            rows = browser.find_elements(By.CSS_SELECTOR, "#items-body tr")
            if not rows:
                return False
            if not all(
                row.find_elements(By.TAG_NAME, "td")[2].text == "Category B"
                for row in rows
            ):
                return False
            return rows

        rows = wait.until(filtered_rows)
        table_data = []
        for row in rows:
            cells = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
            table_data.append(
                {
                    "id": int(cells[0]),
                    "name": cells[1],
                    "category": cells[2],
                    "value": float(cells[3]) if cells[3] else None,
                    "active": cells[4],
                }
            )

        result = pd.DataFrame(table_data)
        output_path = PROCESSED_DIR / "selenium_items.csv"
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        result.to_csv(output_path, index=False)
        print(f"Строк после фильтра Category B: {len(result)}")
        print(f"Результаты Selenium сохранены: {output_path}")
        save_statistics(
            {
                "Способ": "Selenium",
                "Количество записей": len(result),
                "Уникальных id": result["id"].nunique(),
                "Время, с": round(time.perf_counter() - started, 4),
                "Есть ошибки": "Нет",
            }
        )
        return result
    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception as error:
                print(f"Не удалось корректно закрыть Selenium: {error}")
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()

def course_4():
    """Run scenarios 1, 2 and 3 on one freshly prepared data set."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    for path in (STATISTICS_PATH, STATISTICS_MARKDOWN_PATH):
        if path.exists():
            path.unlink()

    print("Запуск курса 1: подготовка общего набора данных")
    course_1()
    print("\nЗапуск курса 2: REST API")
    course_2()
    print("\nЗапуск курса 3: Selenium")
    course_3()

    report = pd.read_csv(STATISTICS_PATH)
    print(report.to_string(index=False))
    print(f"Отчет сохранен: {STATISTICS_MARKDOWN_PATH}")
    return report

def console_clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    return


def main():
    while True:
        print("Выберите действие:")
        print("1. Нормализовать данные из CSV, JSON и XML")
        print("2. Выполнить сценарий CRUD через REST API")
        print("3. Выполнить сценарий с Selenium и сохранить таблицу")
        print("4. Вывести статистику")
        print("0. Выход")
        switch = input("Введите номер действия: ")
        match switch:
            case "1":
                print("Вы выбрали действие 1")
                console_clear()
                course_1()
            case "2":
                print("Вы выбрали действие 2")
                console_clear()
                course_2()
            case "3":
                print("Вы выбрали действие 3")
                console_clear() 
                course_3()
            case "4":
                print("Вы выбрали действие 4")
                console_clear()
                course_4()
            case "0":
                print("Выход из программы")

                time.sleep(1)
                break
            case _:
                print("Неверный выбор")
                
    return

if __name__ == "__main__":
    main()