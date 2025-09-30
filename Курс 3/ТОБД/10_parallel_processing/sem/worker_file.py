import rand_csv
def worker(input_queue, output_queue, worker_id): # Рабочий процесс, который берет задания из входной очереди и кладет результаты в выходную

    while True:
        # Берем задание из очереди
        task = input_queue.get()
        
        # Проверяем сигнал завершения
        if task is None:
            print(f"Рабочий процесс {worker_id} завершает работу")
            break
            
        # Извлекаем параметры задания
        length, pos, time_start, time_end = task
        
        # Выполняем работу
        rand_csv.rand_csv(length, pos, time_start, time_end, output_queue)
