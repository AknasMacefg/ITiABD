import time

def mul_task(x): # Возведение в квадрат с задержкой
    time.sleep(0.5)
    return x * x

def worker_time(task_queue, result_queue): #Берет задачи из очерещди и результат кладет в другую очередь
    while True:
        x = task_queue.get()
        if x is None:   # сигнал остановки
            break
        result = mul_task(x)
        result_queue.put(result)
