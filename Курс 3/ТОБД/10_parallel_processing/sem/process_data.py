from datetime import datetime, timedelta
def process_date(date_str):
    """Функция обработки даты — здесь просто парсинг и возврат дня недели."""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    time.sleep(0.3)  # имитация тяжёлой работы
    return date_str, date_obj.strftime("%A")  # (дата, день недели)
