from datetime import date
from typing import Optional, Tuple

from .models import Employee


def get_nearest_birthday_employee(
    today: Optional[date] = None,
) -> Optional[Tuple[Employee, int]]:
    """Возвращает пару (пользователь, дней_до) с ближайшим днём рождения.

    Игнорирует пользователей без даты рождения. Если никого нет — возвращает None.
    """
    if today is None:
        today = date.today()

    employees = Employee.objects.exclude(birth_date__isnull=True)
    nearest_employee: Optional[Employee] = None
    nearest_days: Optional[int] = None

    for employee in employees:
        birth_date = employee.birth_date
        if birth_date is None:
            continue
        days = _days_until_next_birthday(birth_date, today)
        if nearest_days is None or days < nearest_days:
            nearest_employee = employee
            nearest_days = days

    if nearest_employee is None or nearest_days is None:
        return None

    return nearest_employee, nearest_days


def serialize_employee_nearest_payload(employee: Employee, days_until: int) -> dict:
    """Готовит полезную нагрузку для клиента по вебсокету."""
    return {
        "employee_name": employee.name,
        "birth_date": employee.birth_date.isoformat() if employee.birth_date else None,
        "days_until": days_until,
    }


def _days_until_next_birthday(birth_date: date, today: date) -> int:
    """Возвращает количество дней до ближайшего дня рождения от today.

    Если ДР сегодня — возвращает 0.
    """

    next_birthday_year = today.year
    try:
        next_birthday = birth_date.replace(year=next_birthday_year)
    except ValueError:
        # На случай 29 февраля: переносим на 28 в не високосный год
        if birth_date.month == 2 and birth_date.day == 29:
            next_birthday = date(next_birthday_year, 2, 28)
        else:
            raise

    if next_birthday < today:
        next_birthday_year += 1
        try:
            next_birthday = birth_date.replace(year=next_birthday_year)
        except ValueError:
            if birth_date.month == 2 and birth_date.day == 29:
                next_birthday = date(next_birthday_year, 2, 28)
            else:
                raise

    return (next_birthday - today).days
