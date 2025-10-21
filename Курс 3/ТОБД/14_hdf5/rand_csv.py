import random
import time

#генератор случайной даты и числа
def rand_csv(length, pos, time_start, time_end, output): 
    csv_rows = []
    for i in range(length):
        stime = time.mktime(time.strptime(time_start, '%m/%d/%Y %I:%M %p'))
        etime = time.mktime(time.strptime(time_end, '%m/%d/%Y %I:%M %p'))
        ptime = stime + random.random() * (etime - stime)
        csv_rows.append([time.strftime('%y%m%d%H%M%S', time.localtime(ptime)), random.randint(1, 9999999), pos])
    output.put(csv_rows)
