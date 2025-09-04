
sudoku = [ 
[5,3,'','',7,'','','',''],
[6,'','',1,9,5,'','',''],
['',9,8,'','','','',6,''],
[8,'','','',6,'','','',3],
[4,'','',8,'',3,'','',1],
[7,'','','',2,'','','',6],
['',6,'','','','',2,8,''],
['','','',4,1,9,'','',5],
['','','','',8,'','',7,9] ]


def valid_check(sudoku):
    for row in range(9):
        for col in range(9):
            k = sudoku[row][col]
            if k == '': continue

            for j in range(9):
                if j != col and sudoku[row][j] == k:
                    return False

            for i in range(9):
                if i != row and sudoku[i][col] == k:
                    return False

            start_row = (row // 3) * 3
            start_col = (col // 3) * 3
            for i in range(3):
                for j in range(3):
                    r = start_row + i
                    c = start_col + j
                    if sudoku[r][c] == '': continue
                    if (r != row or c != col) and sudoku[r][c] == k:
                        return False

    return True

if (valid_check(sudoku) == True):
    print("Cудоку заполнена правильно!")
else:
    print("Судоку заполнена неправильно!")

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

print("НОК чисел 21 и 7: ", lcm(21, 7))   

def lis(arr):
    max_value = 0
    max_arr = []
    for i in range(0, len(arr)):
        long_arr = []
        long_arr.append(arr[i])
        temp_i = i
        for j in range(0, len(arr)):
            if arr[temp_i] < arr[j] and j > temp_i:
                temp_i = j
                long_arr.append(arr[j])
            else:
                continue
        if (len(long_arr) > max_value):
            max_value = len(long_arr)
            max_arr = long_arr
    return max_value, max_arr

print('Наибольшая возрастающая последовательности в массиве: ', lis([50, 3, 10, 7, 40, 80]))
            