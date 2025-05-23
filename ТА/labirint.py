from collections import deque

labirint = [
    [1, 1, 1, 1],
    [0, 1, 0, 1],
    [1, 1, 1, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1]
]

n, m = len(labirint), len(labirint[0])
start = (0, 0)
end = (n - 1, m - 1)
def is_valid(x, y):
    return 0 <= x < n and 0 <= y < m and labirint[x][y] == 1
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

queue = deque()
queue.append((start[0], start[1], [start]))

visited = [[False] * m for _ in range(n)]
visited[start[0]][start[1]] = True

found = False

while queue and not found:
    x, y, path = queue.popleft()

    if (x, y) == end:
        print("Кратчайший путь:", path)
        found = True
        break

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny) and not visited[nx][ny]:
            visited[nx][ny] = True
            queue.append((nx, ny, path + [(nx, ny)]))

if not found:
    print("Путь не найден.")