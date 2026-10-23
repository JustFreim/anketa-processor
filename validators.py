#проверки полей анкеты ФИО, почта, телефон, группа


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


if __name__ == "__main__":
    #проверка модуля при прямом запуске validators.py
    print(parsLine("иванов иван;ivanov@mail.ru;89211112233;09с33"))
