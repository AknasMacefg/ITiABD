import time
import random

def rand_csv(length, pos, time_start, time_end, output): #генератор случайно даты и числа
    csv_rows = []
    for i in range(length):
        stime = time.mktime(time.strptime(time_start, '%m/%d/%Y %I:%M %p'))
        etime = time.mktime(time.strptime(time_end, '%m/%d/%Y %I:%M %p'))
        ptime = stime + random.random() * (etime - stime)
        csv_rows.append([time.strftime('%y%m%d%H%M%S', time.localtime(ptime)), random.randint(1, 9999999), pos])
    output.put(csv_rows)

def worker_time(task_queue, result_queue): #Берет задачи из очерещди и результат кладет в другую очередь
    while True:
        x = task_queue.get()
        if x is None:   # сигнал остановки
            break
        result = rand_csv(random.randint(50000,500000), x, "1/1/2008 1:30 PM", "1/1/2025 4:50 AM", result_queue)
        result_queue.put(result)
