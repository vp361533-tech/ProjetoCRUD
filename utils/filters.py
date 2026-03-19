# utils/filters.py

from datetime import datetime

def format_datetime_br(value):
    if not value:
        return ""

    dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%d/%m/%Y às %H:%M")