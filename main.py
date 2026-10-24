#обработчик анкет: точка входа

from validators import parsLine
from report import printTable, printBad, printStat
from storage import readLines, saveFiles, OK_FILE, ERR_FILE

INPUT_FILE = "data/anketa.txt"


def main():
    lines = readLines(INPUT_FILE)
    if lines is None:
        print("Файл", INPUT_FILE, "не найден. Он должен лежать в data/")
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


if __name__ == "__main__":
    main()
