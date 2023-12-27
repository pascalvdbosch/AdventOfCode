class MyClass(object):
    def __init__(self, a, b):
        self.a = min([a, b])
        self.b = max([a, b])
    def __hash__(self):
        global N
        return self.a * N + self.b
    def __eq__(self, other):
        return isinstance(other, MyClass)
    def __str__(self):
        return str(self.a) + "-" + str(self.b)
    def __repr__(self):
        return str(self.a) + "-" + str(self.b)

with open('input5.txt', 'r') as i:
    data0 = { (line[:line.index(":")]): list(s.strip() for s in line[line.index(":")+1:].strip().split(' ')) for line in i.readlines()}
    names = list(set(w for v in data0.values() for w in v).union(set(data0.keys())))
    global N
    N = len(names)
    edges = set()
    for aname in data0:
        a = names.index(aname)
        for bname in data0[aname]:
            b = names.index(bname)
            edges.add(MyClass(a, b))

M = len(edges) # number of edges

graph = { key: list(filter(lambda i: i is not None, map(lambda i: i.b if i.a == key else (i.a if i.b == key else None), edges))) for key in range(N) }

# dit is het dijkstra algoritme: https://stackoverflow.com/a/63977021
from heapq import heappop, heappush
def dijkstra(adjList, source, sink):
    n = len(adjList)
    parent = [None]*n
    heap = [(0, source, 0)] # No need to push all nodes on the heap at the start
    # only add the source to the heap

    while heap:
        distance, current, came_from = heappop(heap)
        if parent[current] is not None:  # skip if already visited
            continue
        parent[current] = came_from  # this also marks the node as visited
        if sink and current == sink:  # only correct place to have terminating condition
            # build path
            path = [current]
            while current != source:
                current = parent[current]
                path.append(current)
            path.reverse()
            return distance, path
        for (neighbor, cost) in adjList[current]:
            if parent[neighbor] is None:  # not yet visited
                heappush(heap, (distance + cost, neighbor, current))

graph_ = [[]] + list(list(filter(lambda x: x is not None, list([j + 1, 1] if MyClass(i, j) in edges else None for j in range(N)))) for i in range(N))

import random

def connected(without):
    todo = [0]
    done = set()
    while len(todo) > 0:
        take = todo.pop()
        for next in graph[take]:
            if MyClass(take, next) in without: continue
            if next not in done:
                todo += [next]
        done.add(take)
    return len(done)

ret = { e: 0 for e in edges }

for I in range(2000):
    i = random.randint(0, N - 1)
    j = random.randint(0, N - 1)
    if i != j:
        dist, path = dijkstra(graph_, i + 1, j + 1)
        path = [p - 1 for p in path]
        for a, b in list(zip(path[:-1], path[1:])):
            ret[MyClass(a, b)] += 1

top = sorted(ret, key=ret.get, reverse=True)[:3]

c = connected(set(top))
print(c * (N - c))
