#вывод: таблица принятых анкет, список брака, статистика

W_FIO = 28 #ширины колонок таблицы
W_MAIL = 24
W_PHONE = 20


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


if __name__ == "__main__":
    #проверка модуля при прямом запуске: python report.py
    demo = [{"fio": "Иванов Иван Петрович", "mail": "ivanov@mail.ru",
             "phone": "+7 (921) 111-22-33", "group": "09с33"}]
    printTable(demo)
