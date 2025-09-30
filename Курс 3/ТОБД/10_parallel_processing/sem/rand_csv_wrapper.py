import multiprocessing as mp
import rand_csv

def rand_csv_wrapper(args): #Обертка для функции rand_csv для использования с Pool
    length, pos, time_start, time_end = args
    # Создаем временную очередь для совместимости с существующей функцией
    temp_queue = mp.Queue()
    rand_csv.rand_csv(length, pos, time_start, time_end, temp_queue)
    return temp_queue.get()
