import requests
import time
import random
import sys
from datetime import datetime
from tqdm import tqdm

# ---------- НАСТРОЙКИ ----------
START_ID = 1_000_000          # начало диапазона
END_ID   = 1_010_000          # конец диапазона
DELAY_MIN = 0.3               # минимальная задержка между запросами (сек)
DELAY_MAX = 0.8               # максимальная задержка
TIMEOUT = 10                  # таймаут запроса
LOG_FILE = "found_videos.txt" # файл, куда записываются найденные видео
BEEP = False                   # звуковой сигнал при находке (Windows)
# --------------------------------

OEMBED_URL = "https://vimeo.com/api/oembed.json"


def beep():
    """Издаёт короткий звуковой сигнал (только Windows)."""
    if BEEP and sys.platform.startswith("win"):
        import winsound
        winsound.Beep(1000, 300)  # частота 1000 Гц, длительность 300 мс


def notify(video_id: int, title: str = ""):
    """
    Уведомление о найденном видео:
    - вывод в консоль с временной меткой;
    - звуковой сигнал;
    - запись в лог-файл.
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] ✅ НАЙДЕНО ВИДЕО: https://vimeo.com/{video_id}"
    if title:
        line += f"  |  {title}"

    # Печатаем поверх прогресс-бара
    tqdm.write(line)

    # Звук
    beep()

    # Запись в файл
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def check_video(video_id: int):
    """
    Возвращает (exists, title):
        exists — True, если видео существует;
        title  — название видео (если удалось получить).
    """
    params = {"url": f"https://vimeo.com/{video_id}"}
    try:
        resp = requests.get(OEMBED_URL, params=params, timeout=TIMEOUT)

        if resp.status_code == 200:
            try:
                data = resp.json()
                title = data.get("title", "")
            except ValueError:
                title = ""
            return True, title

        elif resp.status_code == 404:
            return False, ""

        elif resp.status_code == 429:
            tqdm.write(f"\n[!] Rate limit (429) на ID {video_id}. Пауза 60 сек...")
            time.sleep(60)
            return check_video(video_id)

        else:
            return False, ""

    except requests.RequestException as e:
        tqdm.write(f"\n[!] Ошибка сети на ID {video_id}: {e}")
        return False, ""


def main():
    total_tested = 0
    valid_count = 0

    print(f"Исследуем диапазон ID: {START_ID} – {END_ID}")
    print(f"Найденные видео будут записаны в: {LOG_FILE}\n")

    for vid in tqdm(range(START_ID, END_ID + 1), desc="Проверка ID"):
        exists, title = check_video(vid)
        total_tested += 1

        if exists:
            valid_count += 1
            notify(vid, title)   # <-- уведомление

        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

    # ---------- РЕЗУЛЬТАТЫ ----------
    density = valid_count / total_tested if total_tested else 0
    print("\n" + "=" * 50)
    print(f"Проверено ID:        {total_tested}")
    print(f"Найдено видео:       {valid_count}")
    print(f"Плотность видео:     {density:.6f} ({density*100:.2f}%)")
    print("=" * 50)

    MAX_POSSIBLE_ID = 10_000_000_000
    estimated_total = density * MAX_POSSIBLE_ID
    print(f"Оценка общего числа видео (при MAX_ID={MAX_POSSIBLE_ID:,}):")
    print(f"  ≈ {estimated_total:,.0f} видео")


if __name__ == "__main__":
    main()