INPUT_FILE = "anketa.txt"
OK_FILE = "ok.txt"
ERR_FILE = "errors.txt"

W_FIO = 28 #ширины колонок таблицы
W_MAIL = 24
W_PHONE = 20

def checkFIO(raw):
    """возвращает ФИО, None или None, причина отказа"""
    parts = raw.split()
    if len(parts) < 2:
        return None, "в ФИО меньше двух слов"
    return " ".join(parts).title(), None

def checkMail(raw):
    """возвращает почта, None или None, причина отказа"""
    mail = raw.strip().lower()
    bad = "почта неверная: " + raw.strip()
    if mail.count("@") != 1:
        return None, bad
    name, domain = mail.split("@")
    if name == "" or "." not in domain:
        return None, bad
    if domain.startswith(".") or domain.endswith("."):
        return None, bad
    return mail, None

def checkPhone(raw):
    """возвращает телефон, None или None, причина отказа"""
    digits = []
    for ch in raw:
        if ch.isdigit():
            digits.append(ch)
    d = "".join(digits)
    if len(d) != 11:
        return None, f"телефон неверный: цифр {len(d)}, нужно 11"
    if d[0] not in "78":
        return None, "телефон неверный: номер должен начинаться с 7 или 8"
    return f"+7 ({d[1:4]}) {d[4:7]}-{d[7:9]}-{d[9:]}", None

def parsLine(line):
    """разбирает строку. Возвращает анкета, None или None, причина"""
    fields = line.split(";")
    if len(fields) != 4:
        return None, f"полей {len(fields)} вместо 4"
    fio, err = checkFIO(fields[0])
    if err:
        return None, err
    mail, err = checkMail(fields[1])
    if err:
        return None, err
    phone, err = checkPhone(fields[2])
    if err:
        return None, err
    group = "".join(fields[3].split()).lower()
    if group == "":
        return None, "группа не указана"
    return {"fio": fio, "mail": mail, "phone": phone, "group": group}, None

def readLines(filename):
    """читает файл. Если файла нет, возвращает None"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return None

def phoneMask(phone):
    return phone[:9] + "***-**-" + phone[-2:]

def fit(text, width):
    if len(text) > width:
        return text[:width - 1] + "~"
    return text

def printTable(good):
    line = "-" * (5 + W_FIO + W_MAIL + W_PHONE + 6)
    print(f"{'№':>3}  {'ФИО':<{W_FIO}}{'Почта':<{W_MAIL}}"
          f"{'Телефон':<{W_PHONE}}Группа")
    print(line)
    for i, a in enumerate(good, 1):
        print(f"{i:>3}  {fit(a['fio'], W_FIO - 1):<{W_FIO}}"
              f"{fit(a['mail'], W_MAIL - 1):<{W_MAIL}}"
              f"{phoneMask(a['phone']):<{W_PHONE}}{a['group']}")
    print(line)

def printBad(bad):
    print("Отклонено строк:", len(bad))
    for num, line, reason in bad:
        print(f"  строка {num}: {reason}")
        print("      " + line)

def printStat(total, empty, good, bad):
    print(f"Всего строк в файле: {total} (пустых пропущено: {empty})")
    print(f"Принято: {len(good)} | Отклонено: {len(bad)}")
    stat = {}
    for a in good:
        stat[a["group"]] = stat.get(a["group"], 0) + 1
    print("\nПо группам:")
    for group in sorted(stat):
        print(f"  {group:<8}{stat[group]}")

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
