from datetime import date


def year(request):
    """Добавляет переменную с текущим годом."""
    current_year = date.today()
    return {
        'year': int(current_year.year),
    }
