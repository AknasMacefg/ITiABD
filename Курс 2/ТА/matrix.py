matrix = [
    [1, 1, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [1, 1, 1, 1, 0],
    [1, 1, 0, 1, 0],
    [1, 1, 0, 1, 1]
]

n = len(matrix)

candidate = 0
for i in range(1, n):
    if matrix[candidate][i] == 1:
        candidate = i

is_celebrity = True
for i in range(n):
    if i == candidate:
        continue
    if matrix[candidate][i] == 1 or matrix[i][candidate] == 0:
        is_celebrity = False
        break

if is_celebrity:
    print("Знаменитость:", candidate + 1)
else:
    print("Знаменитость не найдена")