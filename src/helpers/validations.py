from datetime import datetime

def validate_date(data_str: str) -> bool:

    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False
