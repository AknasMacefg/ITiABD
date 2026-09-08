import argparse
import time

import requests

VIDEO_URL = "https://vimeo.com/{video_id}"
MAX_VIDEO_ID = 2_147_483_647
DEFAULT_BLOCK_SIZE = 1_000_000
DEFAULT_MAX_BLOCKS = 2
DEFAULT_DELAY = 0.2
REQUEST_TIMEOUT = 30
REQUEST_RETRIES = 2

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def video_exists(session, video_id):
    """Return True only for a successful response for a candidate video URL."""
    for attempt in range(REQUEST_RETRIES + 1):
        try:
            print(f"Проверка {video_id} (попытка {attempt + 1})...")
            response = session.get(
                VIDEO_URL.format(video_id=video_id),
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT,
                allow_redirects=True,
            )
            return response.status_code == 200
        except requests.RequestException as error:
            if attempt == REQUEST_RETRIES:
                print(f"Пропуск {video_id}: сервер не ответил ({error})")
                return False
            time.sleep(1)


def run_experiment(start, block_size, max_blocks, delay):
    checked = 0
    found = 0
    block_counts = []

    with requests.Session() as session:
        for block_number in range(max_blocks):
            block_found = 0
            block_start = start + block_number * block_size

            for number in range(block_start, block_start + block_size):
                video_id = str(number)
                if video_exists(session, video_id):
                    block_found += 1
                checked += 1
                if delay:
                    time.sleep(delay)

            found += block_found
            block_counts.append(block_found)
            print(
                f"Диапазон {block_start:,}..{block_start + block_size - 1:,}: "
                f"найдено {block_found} видео"
            )

            if len(block_counts) >= 2:
                previous, current = block_counts[-2:]
                difference = abs(current - previous) / max(previous, 1)
                if difference <= 0.01:
                    break

    density = found / checked if checked else 0
    possible_ids = MAX_VIDEO_ID
    estimate = round(density * possible_ids)

    print(f"Перебрано адресов: {checked}")
    print(f"Обнаружено роликов: {found}")
    print(f"Оценочная доля занятых адресов: {density:.8%}")
    print(f"Примерное общее количество роликов: {estimate:,}")


def parse_video_id(value):
    try:
        video_id = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("ID Vimeo должен быть целым числом") from error

    if video_id < 1 or video_id > MAX_VIDEO_ID:
        raise argparse.ArgumentTypeError(
            f"ID Vimeo должен быть в диапазоне от 1 до {MAX_VIDEO_ID}"
        )
    return video_id


def run_id_range(start_id, end_id, block_size, delay):
    start = start_id
    end = end_id
    if start > end:
        raise ValueError("Начальный ID не может быть больше конечного")

    checked = 0
    found = 0
    total = end - start + 1

    with requests.Session() as session:
        for block_start in range(start, end + 1, block_size):
            block_end = min(block_start + block_size - 1, end)
            block_found = 0

            for number in range(block_start, block_end + 1):
                video_id = str(number)
                if video_exists(session, video_id):
                    block_found += 1
                checked += 1
                if delay:
                    time.sleep(delay)

            found += block_found
            print(
                f"Диапазон {block_start}..{block_end}: "
                f"найдено {block_found} видео"
            )

    density = found / checked if checked else 0
    possible_ids = MAX_VIDEO_ID
    estimate = round(density * possible_ids)

    print(f"Перебрано адресов: {checked} из {total}")
    print(f"Обнаружено роликов: {found}")
    print(f"Оценочная доля занятых адресов: {density:.8%}")
    print(f"Примерное общее количество роликов: {estimate:,}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Оценка числа Vimeo-видео по выборке числовых ID."
    )
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--block-size", type=int, default=DEFAULT_BLOCK_SIZE)
    parser.add_argument("--max-blocks", type=int, default=DEFAULT_MAX_BLOCKS)
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY)
    parser.add_argument("--from-id", type=parse_video_id)
    parser.add_argument("--to-id", type=parse_video_id)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    if (arguments.from_id is None) != (arguments.to_id is None):
        raise SystemExit("Параметры --from-id и --to-id нужно указывать вместе")

    if arguments.from_id is not None:
        try:
            run_id_range(
                arguments.from_id,
                arguments.to_id,
                arguments.block_size,
                arguments.delay,
            )
        except ValueError as error:
            raise SystemExit(error)
    else:
        run_experiment(
            arguments.start,
            arguments.block_size,
            arguments.max_blocks,
            arguments.delay,
        )