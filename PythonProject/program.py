# -*- coding: utf-8 -*-
"""
Программа для стилистического (звёздочного) отображения даты и вычислений с датой.
Использует "текущую" дату: 23 ноября 2025 (как указано в условии).
"""

from datetime import date, datetime

# --- шрифт цифр (7 строк на цифру, 5 столбцов)
DIGITS = {
    '0': [
        " *** ",
        "*   *",
        "*   *",
        "*   *",
        "*   *",
        "*   *",
        " *** "
    ],
    '1': [
        "  *  ",
        " **  ",
        "* *  ",
        "  *  ",
        "  *  ",
        "  *  ",
        "*****"
    ],
    '2': [
        " *** ",
        "*   *",
        "    *",
        "   * ",
        "  *  ",
        " *   ",
        "*****"
    ],
    '3': [
        " *** ",
        "*   *",
        "    *",
        "  ** ",
        "    *",
        "*   *",
        " *** "
    ],
    '4': [
        "   * ",
        "  ** ",
        " * * ",
        "*  * ",
        "*****",
        "   * ",
        "   * "
    ],
    '5': [
        "*****",
        "*    ",
        "*    ",
        " *** ",
        "    *",
        "*   *",
        " *** "
    ],
    '6': [
        " *** ",
        "*   *",
        "*    ",
        "**** ",
        "*   *",
        "*   *",
        " *** "
    ],
    '7': [
        "*****",
        "    *",
        "   * ",
        "  *  ",
        " *   ",
        " *   ",
        " *   "
    ],
    '8': [
        " *** ",
        "*   *",
        "*   *",
        " *** ",
        "*   *",
        "*   *",
        " *** "
    ],
    '9': [
        " *** ",
        "*   *",
        "*   *",
        " ****",
        "    *",
        "*   *",
        " *** "
    ],
    ' ': [  # пробел (для разделения групп)
        "     ",
        "     ",
        "     ",
        "     ",
        "     ",
        "     ",
        "     "
    ]
}

# русские названия дней недели
WEEKDAYS_RU = [
    "понедельник",  # 0
    "вторник",
    "среда",
    "четверг",
    "пятница",
    "суббота",
    "воскресенье"   # 6
]

# фиксируем "сейчас" как 23 ноября 2025 (по условию)
TODAY = date(2025, 11, 23)

# --- функции ----------------------------------------------------------

def is_leap_year(year: int) -> bool:
    """Возвращает True, если год високосный."""
    return (year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))

def day_of_week(day: int, month: int, year: int) -> str:
    """Возвращает день недели на русском для указанной даты."""
    d = date(year, month, day)
    return WEEKDAYS_RU[d.weekday()]

def calculate_age(day: int, month: int, year: int, today: date = TODAY) -> int:
    """Вычисляет количество полных лет на дату today."""
    birth = date(year, month, day)
    age = today.year - birth.year
    # если день/месяц рождения ещё не наступили в текущем году — минус 1
    if (today.month, today.day) < (birth.month, birth.day):
        age -= 1
    return age

def render_star_number_string(s: str, spacing_between_digits: int = 1, spacing_between_groups: int = 2) -> str:
    """
    Рендерит строку из символов (цифры и пробелы) в звёздочный вид.
    spacing_between_digits — пробелы между цифрами,
    spacing_between_groups — дополнительные пробелы между группами (dd mm yyyy).
    """
    rows = [''] * 7
    # будем добавлять символы; поддерживаем пробел как разделитель
    for idx, ch in enumerate(s):
        pattern = DIGITS.get(ch, DIGITS[' '])
        for r in range(7):
            rows[r] += pattern[r]
            # добавляем пробелы между цифрами
            if idx != len(s) - 1:
                # если следующий символ — пробел (группа), добавляем spacing_between_groups, иначе spacing_between_digits
                next_ch = s[idx + 1]
                if next_ch == ' ' or ch == ' ':
                    rows[r] += ' ' * spacing_between_groups
                else:
                    rows[r] += ' ' * spacing_between_digits
    return '\n'.join(rows)

# --- валидация ввода --------------------------------------------------

def read_int(prompt: str, min_v: int, max_v: int) -> int:
    """Читает целое число в диапазоне, повторяя запрос пока не верно."""
    while True:
        try:
            s = input(prompt).strip()
            v = int(s)
            if v < min_v or v > max_v:
                print(f"Ошибка: введите число от {min_v} до {max_v}.")
                continue
            return v
        except ValueError:
            print("Ошибка: введите целое число.")

def valid_date(day: int, month: int, year: int) -> bool:
    """Проверяет, существует ли такая дата."""
    try:
        date(year, month, day)
        return True
    except ValueError:
        return False

# --- основной сценарий ------------------------------------------------

def main():
    print("Введите дату рождения:")
    day = read_int("День (1-31): ", 1, 31)
    month = read_int("Месяц (1-12): ", 1, 12)
    year = read_int("Год (например, 1990): ", 1, 9999)

    if not valid_date(day, month, year):
        print("Ошибка: введённой даты не существует. Проверьте день/месяц/год.")
        return

    dow = day_of_week(day, month, year)
    leap = is_leap_year(year)
    age = calculate_age(day, month, year)

    print()
    print(f"Дата: {day:02d}.{month:02d}.{year:04d}")
    print(f"День недели: {dow}")
    print(f"Високосный год: {'да' if leap else 'нет'}")
    print(f"Сейчас лет: {age} {'год' if (age%10==1 and age%100!=11) else ('года' if 2<=age%10<=4 and (age%100<10 or age%100>=20) else 'лет')}")

    # звездочный вывод в формате "дд мм гггг"
    s_date = f"{day:02d} {month:02d} {year:04d}"
    print("\nДата в звёздочках (формат: дд мм гггг):\n")
    print(render_star_number_string(s_date))

if __name__ == "__main__":
    main()
