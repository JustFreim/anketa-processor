#чтение входного файла и запись результатов

OK_FILE = "ok.txt"
ERR_FILE = "errors.txt"


def readLines(filename):
    """читает файл. Если файла нет, возвращает None"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return None


def saveFiles(good, bad):
    with open(OK_FILE, "w", encoding="utf-8") as f:
        for a in good:
            row = [a["fio"], a["mail"], a["phone"], a["group"]]
            f.write(";".join(row) + "\n")
    with open(ERR_FILE, "w", encoding="utf-8") as f:
        for num, line, reason in bad:
            f.write(f"строка {num}: {reason}\n    {line}\n")


if __name__ == "__main__":
    #проверка модуля при прямом запуске python storage.py
    lines = readLines("data/anketa.txt")
    if lines is None:
        print("Файл не найден")
    else:
        print("Прочитано строк:", len(lines))
