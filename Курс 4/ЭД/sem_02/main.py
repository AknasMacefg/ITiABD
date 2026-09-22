import os
import time
import random
import datetime
import yadisk
import requests

TOKEN = "y0__wgBEML73XsYt6FKIJ6jppAZMIHxpegIxpetHu-NOt_Mg_1Qda6_PEGbpzs" 
REMOTE_FOLDER = "/sem_2_test"           
REMOTE_FILE = f"{REMOTE_FOLDER}/work_file.bin"
LOCAL_FILE = "local_work_file.bin"
FILE_SIZE = 1024 * 1024     
DELAY = 2                          
MIN_DURATION = 300                   


def generate_random_file(path: str, size: int) -> None:
    """Создаёт файл с случайными данными заданного размера."""
    with open(path, "wb") as f:
        f.write(os.urandom(size))
    print(f"[{datetime.datetime.now()}] Сгенерирован файл {path} размером {size} байт")


def check_cloud_availability(client: yadisk.Client) -> bool:
    """
    Проверяет доступность облачной папки и соединения.
    Возвращает True, если папка существует и доступна.
    """
    try:
        client.get_meta(REMOTE_FOLDER)
        return True
    except yadisk.exceptions.PathNotFoundError:
        print(f"[{datetime.datetime.now()}] Папка {REMOTE_FOLDER} не найдена. Попытка создать...")
        try:
            client.mkdir(REMOTE_FOLDER)
            print(f"[{datetime.datetime.now()}] Папка {REMOTE_FOLDER} создана.")
            return True
        except Exception as e:
            print(f"[{datetime.datetime.now()}] Не удалось создать папку: {e}")
            return False
    except (yadisk.exceptions.YaDiskConnectionError,
            yadisk.exceptions.RequestTimeoutError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout) as e:
        print(f"[{datetime.datetime.now()}] Ошибка соединения: {e}")
        return False
    except Exception as e:
        print(f"[{datetime.datetime.now()}] Неизвестная ошибка при проверке папки: {e}")
        return False


def safe_upload(client: yadisk.Client, local_path: str, remote_path: str) -> bool:
    """Загружает файл на Яндекс.Диск с обработкой ошибок."""
    try:
        client.upload(local_path, remote_path, overwrite=True)
        print(f"[{datetime.datetime.now()}] Файл загружен: {local_path} -> {remote_path}")
        return True
    except (yadisk.exceptions.YaDiskConnectionError,
            yadisk.exceptions.RequestTimeoutError,
            yadisk.exceptions.RetriableYaDiskError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout) as e:
        print(f"[{datetime.datetime.now()}] Ошибка загрузки (сеть): {e}")
        return False
    except Exception as e:
        print(f"[{datetime.datetime.now()}] Ошибка загрузки: {e}")
        return False


def safe_download(client: yadisk.Client, remote_path: str, local_path: str) -> bool:
    """Скачивает файл с Яндекс.Диска с обработкой ошибок."""
    try:
        client.download(remote_path, local_path, overwrite=True)
        print(f"[{datetime.datetime.now()}] Файл скачан: {remote_path} -> {local_path}")
        return True
    except (yadisk.exceptions.YaDiskConnectionError,
            yadisk.exceptions.RequestTimeoutError,
            yadisk.exceptions.RetriableYaDiskError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout) as e:
        print(f"[{datetime.datetime.now()}] Ошибка скачивания (сеть): {e}")
        return False
    except Exception as e:
        print(f"[{datetime.datetime.now()}] Ошибка скачивания: {e}")
        return False


def main():
    start_time = time.time()
    print(f"[{datetime.datetime.now()}] Программа запущена. Минимальное время работы: {MIN_DURATION} сек.")

    with yadisk.Client(token=TOKEN) as client:
        if not check_cloud_availability(client):
            print("Не удалось установить соединение с облаком. Программа будет повторять попытки.")

        iteration = 0
        while time.time() - start_time < MIN_DURATION:
            iteration += 1
            print(f"\n--- Итерация {iteration} ---")
            try:
                generate_random_file(LOCAL_FILE, FILE_SIZE)
            except OSError as e:
                print(f"[{datetime.datetime.now()}] Ошибка записи локального файла: {e}")
                time.sleep(DELAY)
                continue
            if not check_cloud_availability(client):
                print(f"[{datetime.datetime.now()}] Облако недоступно. Пропуск итерации.")
                time.sleep(DELAY)
                continue
            if not safe_upload(client, LOCAL_FILE, REMOTE_FILE):
                time.sleep(DELAY)
                continue
            time.sleep(DELAY)
            if not safe_download(client, REMOTE_FILE, LOCAL_FILE):
                time.sleep(DELAY)
                continue
            time.sleep(DELAY)
            print(f"[{datetime.datetime.now()}] Рабочий файл перезаписан (скачан из облака).")

        print(f"\n[{datetime.datetime.now()}] Программа завершена. Отработано {time.time() - start_time:.1f} сек.")


if __name__ == "__main__":
    main()