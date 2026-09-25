# -*- coding: utf-8 -*-
import os
import sys
import time
import ctypes
from ctypes import wintypes

OUTPUT_FILE = "files_info.tsv"

# ---------- Windows API ----------
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

FILE_READ_ATTRIBUTES = 0x0080
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
FILE_SHARE_DELETE = 0x00000004
OPEN_EXISTING = 3
FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
FileBasicInfo = 0

INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value


class FILE_BASIC_INFO(ctypes.Structure):
    _fields_ = [
        ("CreationTime", ctypes.c_longlong),
        ("LastAccessTime", ctypes.c_longlong),
        ("LastWriteTime", ctypes.c_longlong),
        ("ChangeTime", ctypes.c_longlong),
        ("FileAttributes", ctypes.c_uint32),
    ]


kernel32.CreateFileW.argtypes = [
    wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
    wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
]
kernel32.CreateFileW.restype = wintypes.HANDLE

kernel32.GetFileInformationByHandleEx.argtypes = [
    wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD,
]
kernel32.GetFileInformationByHandleEx.restype = wintypes.BOOL

kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
kernel32.CloseHandle.restype = wintypes.BOOL

kernel32.GetLogicalDrives.restype = wintypes.DWORD

WINDOWS_TICK = 10000000
SEC_TO_UNIX_EPOCH = 11644473600


def filetime_to_unix(ft):
    if not ft:
        return 0
    return int(ft // WINDOWS_TICK - SEC_TO_UNIX_EPOCH)


def get_win_times(path):
    handle = kernel32.CreateFileW(
        path,
        FILE_READ_ATTRIBUTES,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        None,
        OPEN_EXISTING,
        FILE_FLAG_BACKUP_SEMANTICS | FILE_FLAG_OPEN_REPARSE_POINT,
        None,
    )
    if handle == INVALID_HANDLE_VALUE:
        return None
    try:
        info = FILE_BASIC_INFO()
        ok = kernel32.GetFileInformationByHandleEx(
            handle, FileBasicInfo, ctypes.byref(info), ctypes.sizeof(info)
        )
        if not ok:
            return None
        return (
            filetime_to_unix(info.LastAccessTime),
            filetime_to_unix(info.LastWriteTime),
            filetime_to_unix(info.ChangeTime),
        )
    finally:
        kernel32.CloseHandle(handle)


def get_drives():
    mask = kernel32.GetLogicalDrives()
    drives = []
    for i in range(26):
        if mask & (1 << i):
            root = f"{chr(ord('A') + i)}:\\"
            if os.path.exists(root):
                drives.append(root)
    return drives


PERIODS = [
    ("день", 24 * 60 * 60),
    ("месяц", 30 * 24 * 60 * 60),
    ("квартал", 90 * 24 * 60 * 60),
    ("год", 365 * 24 * 60 * 60),
]

ACCESS_PERIODS = [
    ("день", 24 * 60 * 60),
    ("месяц", 30 * 24 * 60 * 60),
    ("год", 365 * 24 * 60 * 60),
]


# ---------- Индикатор прогресса ----------
class Progress:
    """Печатает строку прогресса в stderr не чаще, чем раз в `interval` секунд."""

    def __init__(self, interval=0.2, stream=sys.stderr):
        self.interval = interval
        self.stream = stream
        self.last = 0.0
        self.total = 0
        self.files = 0
        self.dirs = 0
        self.errors = 0
        self.started = time.time()
        self._last_len = 0

    def tick(self, path="", force=False):
        now = time.time()
        if not force and (now - self.last) < self.interval:
            return
        self.last = now

        elapsed = now - self.started
        rate = self.total / elapsed if elapsed > 0 else 0

        # Обрезаем путь, чтобы строка не "прыгала" слишком сильно
        max_path = 60
        shown_path = path
        if len(shown_path) > max_path:
            shown_path = "..." + shown_path[-(max_path - 3):]

        line = (
            f"[{elapsed:7.1f}s] всего: {self.total:>8} "
            f"(файлов: {self.files}, каталогов: {self.dirs}, ошибок: {self.errors}) "
            f"{rate:8.0f}/с  {shown_path}"
        )

        # Дополняем пробелами, чтобы стереть остатки предыдущей строки
        pad = max(0, self._last_len - len(line))
        self.stream.write("\r" + line + " " * pad)
        self.stream.flush()
        self._last_len = len(line)

    def clear(self):
        if self._last_len:
            self.stream.write("\r" + " " * self._last_len + "\r")
            self.stream.flush()
            self._last_len = 0


def main():
    roots = sys.argv[1:] if len(sys.argv) > 1 else get_drives()
    if not roots:
        print("Не найдено доступных дисков.")
        return

    now = time.time()

    total_objects = 0
    total_files = 0
    total_dirs = 0
    errors = 0
    fallback_times = 0

    mod_counts = {name: 0 for name, _ in PERIODS}
    acc_counts = {name: 0 for name, _ in ACCESS_PERIODS}

    progress = Progress(interval=0.2)

    def onerror(e):
        nonlocal errors
        errors += 1
        progress.errors = errors
        progress.tick(getattr(e, "filename", "") or "")

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8", errors="replace") as out:
            out.write("path\tsize\tatime\tmtime\tctime\n")

            for root in roots:
                progress.tick(f"scan {root}", force=True)

                for dirpath, dirnames, filenames in os.walk(
                    root, topdown=True, onerror=onerror, followlinks=False,
                ):
                    objects = [(dirpath, False)]
                    objects += [(os.path.join(dirpath, f), True) for f in filenames]

                    for path, is_file in objects:
                        try:
                            st = os.stat(path, follow_symlinks=False)
                            size = st.st_size

                            times = get_win_times(path)
                            if times is None:
                                times = (
                                    int(st.st_atime),
                                    int(st.st_mtime),
                                    int(st.st_ctime),
                                )
                                fallback_times += 1

                            atime, mtime, ctime = times
                        except OSError:
                            errors += 1
                            progress.errors = errors
                            progress.tick(path)
                            continue

                        total_objects += 1
                        progress.total = total_objects

                        if is_file:
                            total_files += 1
                            progress.files = total_files

                            for name, seconds in PERIODS:
                                age = now - mtime
                                if 0 <= age <= seconds:
                                    mod_counts[name] += 1

                            for name, seconds in ACCESS_PERIODS:
                                age = now - atime
                                if 0 <= age <= seconds:
                                    acc_counts[name] += 1
                        else:
                            total_dirs += 1
                            progress.dirs = total_dirs

                        out.write(f"{path}\t{size}\t{atime}\t{mtime}\t{ctime}\n")

                        progress.tick(path)
    except KeyboardInterrupt:
        progress.clear()
        print("\nПрервано пользователем. Выводятся частичные результаты.", file=sys.stderr)

    progress.clear()

    print(f"Всего объектов: {total_objects}")
    print(f"Файлов: {total_files}")
    print(f"Каталогов: {total_dirs}")
    print(f"Ошибок доступа/обработки: {errors}")
    print(f"Использован резервный источник времени: {fallback_times}")
    print()

    print("Изменённые файлы:")
    for name, _ in PERIODS:
        n = mod_counts[name]
        pct = (n / total_files * 100) if total_files else 0
        print(f"  за последний {name}: {n} ({pct:.2f}% от всех файлов)")

    print()
    print("Файлы, к которым был доступ:")
    for name, _ in ACCESS_PERIODS:
        n = acc_counts[name]
        pct = (n / total_files * 100) if total_files else 0
        print(f"  за последний {name}: {n} ({pct:.2f}% от всех файлов)")

    print()
    print(f"Подробная информация записана в файл: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()