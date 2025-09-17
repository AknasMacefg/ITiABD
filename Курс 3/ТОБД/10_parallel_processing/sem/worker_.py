import avg_count_ 
def worker(input_queue, output_queue): # Функция-обработчик для каждого процесса
    while True:
        filename = input_queue.get()
        
        if filename is None:
            break
        
        avg_count_.avg_count(filename, output_queue)
