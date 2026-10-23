from validators import parsLine
from report import printTable, printBad, printStat

INPUT_FILE = "anketa.txt"
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


def main():
    lines = readLines(INPUT_FILE)
    if lines is None:
        print("Файл", INPUT_FILE, "не найден. Он должен быть рядом с main.py")
        return
    good = []
    bad = []
    empty = 0
    for num, line in enumerate(lines, 1):
        if line.strip() == "":
            empty += 1
            continue
        card, reason = parsLine(line)
        if reason is None:
            good.append(card)
        else:
            bad.append((num, line.strip(), reason))
    good.sort(key=lambda a: a["fio"])
    printTable(good)
    print()
    printBad(bad)
    print()
    printStat(len(lines), empty, good, bad)
    saveFiles(good, bad)
    print(f"\nСохранено: {OK_FILE} и {ERR_FILE}")


main()
