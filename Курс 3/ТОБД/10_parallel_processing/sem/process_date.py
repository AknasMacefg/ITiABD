from datetime import datetime, timedelta
import time
def process_date(date_str): # Функция обработки даты
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    time.sleep(0.3)  # имитация работы
    return date_str, date_obj.strftime("%A")  # (дата, день недели)
