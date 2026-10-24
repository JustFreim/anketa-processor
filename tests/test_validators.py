from validators import checkFIO, checkMail, checkPhone, parsLine


def test_fio_extra_spaces_and_case():
    assert checkFIO("  иванов   иВАН петрович ") == ("Иванов Иван Петрович", None)


def test_fio_one_word_is_bad():
    fio, err = checkFIO("сидоров")
    assert fio is None
    assert err == "в ФИО меньше двух слов"


def test_mail_lowercase_and_strip():
    assert checkMail(" IvAnov@Mail.Ru ") == ("ivanov@mail.ru", None)


def test_mail_without_at_is_bad():
    mail, err = checkMail("kuznetsov.mail.ru")
    assert mail is None
    assert err.startswith("почта неверная")


def test_mail_domain_ends_with_dot_is_bad():
    mail, err = checkMail("fedorov@mail.ru.")
    assert mail is None


def test_phone_is_normalized():
    assert checkPhone("8 921 555 44 33") == ("+7 (921) 555-44-33", None)


def test_phone_wrong_length_is_bad():
    phone, err = checkPhone("+7921123")
    assert phone is None
    assert "цифр 7" in err


def test_phone_wrong_first_digit_is_bad():
    phone, err = checkPhone("+19215556677")
    assert phone is None


def test_parse_line_good():
    card, err = parsLine("петрова анна;petrova@yandex.ru;89217654321;09 С33")
    assert err is None
    assert card == {"fio": "Петрова Анна", "mail": "petrova@yandex.ru",
                    "phone": "+7 (921) 765-43-21", "group": "09с33"}


def test_parse_line_wrong_field_count():
    card, err = parsLine("волков денис;volkov@mail.ru;+79219998877")
    assert card is None
    assert err == "полей 3 вместо 4"
