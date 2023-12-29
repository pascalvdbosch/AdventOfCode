
with open('input7B.txt', 'r') as i:
    data = list(list(line.strip()) for line in i.readlines())

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
        if data[y][x] in '.S':
            if data[y][x] == 'S': start = enc(y, x)
            if y >     0 and data[y - 1][x] == '.': l += [enc(y - 1, x)]
            if y < h - 1 and data[y + 1][x] in '.': l += [enc(y + 1, x)]
            if x >     0 and data[y][x - 1] in '.': l += [enc(y, x - 1)]
            if x < w - 1 and data[y][x + 1] in '.': l += [enc(y, x + 1)]
            graph[enc(y, x)] = l

nodes = set(graph.keys())

print(graph)

# CHATGPT: Give Python code to find the distance to all nodes from a starting node. 
# The input is a dictionary with nodes as keys and list of connected nodes as values. 
import heapq
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance > distances[current_node]: continue
        for neighbor in graph[current_node]:
            distance = current_distance + 1
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    return distances

N = 64

result = dijkstra(graph, start)
meet = [key for key, val in result.items() if val <= N and (N - val) % 2 == 0]
print(len(meet))