from datetime import datetime


def convert_to_date(value):
    date_format = '%Y-%m-%d'
    try:
        return datetime.strptime(value, date_format).date()
    except:
        return None
