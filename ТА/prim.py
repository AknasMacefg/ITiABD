import heapq

def prim(graph, start):
    mst = []  # Список рёбер в минимальном остовном дереве
    visited = set([start])  # Посещённые вершины
    edges = [(weight, start, to) for to, weight in graph[start]]
    heapq.heapify(edges)

    while edges:
        weight, frm, to = heapq.heappop(edges)
        if to not in visited:
            visited.add(to)
            mst.append((frm, to, weight))
            for next_to, next_weight in graph[to]:
                if next_to not in visited:
                    heapq.heappush(edges, (next_weight, to, next_to))

    return mst


graph = {
    'A': [('B', 1), ('C', 3)],
    'B': [('A', 1), ('C', 1), ('D', 5)],
    'C': [('A', 3), ('B', 1), ('D', 4)],
    'D': [('B', 5), ('C', 4)]
}

mst = prim(graph, 'A')
for edge in mst:
    print(edge)