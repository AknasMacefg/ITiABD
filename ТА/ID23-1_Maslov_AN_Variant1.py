
sudoku = [[1,9,3,4,5,6,7,8,9],
          [2,1,2,3,4,5,6,7,8],
          [3,3,1,2,3,4,5,6,7],
          [4,4,4,1,2,3,4,5,6],
          [5,5,5,5,1,2,3,4,5],
          [6,6,6,6,6,1,2,3,4],
          [7,7,7,7,7,7,1,2,3],
          [8,8,8,8,8,8,8,1,2],
          [9,9,9,9,9,9,9,9,1]]


def rows_check(sudoku):
    for i in sudoku:
        for j in i:
            counter = 0
            if (j == 0): continue
            for k in i:
                if (k == 0): continue
                if (j == k):
                    if (counter == 1):
                        return False
                    counter = counter + 1
    return True

def columns_check(sudoku):
    for i in range(0, len(sudoku[0])-1):
        for j in range(0, len(sudoku[0])-1):
            if (sudoku[j][i] == 0): continue
            counter = 0
            for k in range(0, len(sudoku[0])-1):
                if (sudoku[k][i] == 0): continue
                if (sudoku[j][i] == sudoku[k][i]):
                    if (counter == 1):
                        return False
                    counter = counter + 1
    return True

def three_x_three_check(sudoku):
    for i in range(0, len(sudoku[0]) * len(sudoku) ):
        print(i)
    return True

print(rows_check(sudoku))
print(columns_check(sudoku))
print(three_x_three_check(sudoku))

                