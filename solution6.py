
for part2 in [False, True]:
    with open('input6.txt', 'r') as i:
        data = list(list((line.replace("^", ".").replace("v", ".").replace("<", ".").replace(">", ".") if part2 else line).strip()) for line in i.readlines())

    h = len(data)
    w = len(data[0])

    graph = {}

    def enc(y, x):
        return x * h + y
    def dec(v):
        return [v % h, v // h]
    ends = []
    for y in range(h):
        for x in range(w):
            l = []
            if data[y][x] == '.':
                if y == 0 or y == h - 1: ends += [enc(y, x)]
                if y >     0 and data[y - 1][x] == '^': l += [[enc(y - 2, x), 2]]
                if y >     0 and data[y - 1][x] == '.': l += [[enc(y - 1, x), 1]]
                if y < h - 1 and data[y + 1][x] in 'v': l += [[enc(y + 2, x), 2]]
                if y < h - 1 and data[y + 1][x] in '.': l += [[enc(y + 1, x), 1]]
                if x >     0 and data[y][x - 1] in '<': l += [[enc(y, x - 2), 2]]
                if x >     0 and data[y][x - 1] in '.': l += [[enc(y, x - 1), 1]]
                if x < w - 1 and data[y][x + 1] in '>': l += [[enc(y, x + 2), 2]]
                if x < w - 1 and data[y][x + 1] in '.': l += [[enc(y, x + 1), 1]]
                graph[enc(y, x)] = l

    nodes = set(graph.keys())

    def connected(a): # directed!
        return [i for i, __ in graph[a]]
    def get(a, b): # directed!
        return list(i for i in graph[a] if i[0] == b)[0]
    def value(a, b): # directed!
        return get(a, b)[1]

    # I) find b -> c, where b always go to c, and not back and remove by c
    # II) find a <-> b (<)-> c, replace by a (<)-> c

    found = True
    while found:
        found = False
        for b in nodes:    
            if b in ends: continue
            ac = connected(b)
            if len(ac) == 1: 
                c = ac[0]
                if b in connected(c): continue 
                nodes.remove(b)
                bc = value(b, c)
                graph.pop(b)
                for node in nodes:
                    if b in connected(node):
                        nodeb = value(node, b)
                        graph[node].remove(get(node, b))
                        graph[node] += [[c, nodeb + bc]]
                found = True
            elif len(ac) == 2:
                for _ in range(2):
                    ac = list(reversed(ac))
                    a, c = ac
                    if b not in connected(a): continue
                    biway = b in connected(c)
                    nodes.remove(b)
                    ab = value(a, b)
                    ba = value(b, a)
                    bc = value(b, c)
                    cb = value(c, b) if biway else None
                    graph.pop(b)
                    graph[a].remove(get(a, b))
                    if biway: graph[c].remove(get(c, b))
                    graph[a] += [[c, ab + bc]]
                    if biway: graph[c] += [[a, cb + ba]]
                    found = True
                    break
            if found: break

    nodes = list(graph.keys())
    N = len(nodes)

    graph = { node: list([nodes.index(node2), -weight] for node2, weight in graph[nodes[node]]) for node in range(N) }

    graph[N - 1] = []

    def recur(at, weight, visited):
        if at == N - 1:
            return weight
        ret = 0
        for next, weight_extra in graph[at]:
            if next not in visited:
                val = recur(next, weight + weight_extra, visited + [at])
                if val < ret: ret = val
        return ret

    print("Solution: " + str(-recur(0, 0, [])))