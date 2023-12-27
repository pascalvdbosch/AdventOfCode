with open('input3.txt', 'r') as i:
    d = [line.strip() for line in i.readlines()]

w = len(d[0])
h = len(d)
# first y then x
total = 0
for y in range(h):
    for x in range(w):
        if d[y][x] in '0123456789' and (x == 0 or d[y][x-1] not in '0123456789'):
            suc = False
            num = ""
            while x != w and d[y][x] in '0123456789':
                num += d[y][x]
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dy == 0 and dx == 0: continue
                        x2 = x + dx
                        y2 = y + dy
                        if x2 < 0 or x2 >= w or y2 < 0 or y2 >= h: continue
                        if d[y2][x2] not in '0123456789.': 
                            suc = True
                x += 1
            if suc: total += int(num)

print(total)

def getnum(x, y):
    if d[y][x] not in '0123456789': return None
    while x < w and d[y][x] in '0123456789':
        x += 1
    x -= 1
    x2 = x + 1
    while x >= 0 and d[y][x] in '0123456789':
        x -= 1
    x += 1
    x1 = x
    return int(d[y][x1:x2])

total2 = 0
for y in range(h):
    for x in range(w):
        if d[y][x] == "*":
            left = getnum(x - 1, y)
            right = getnum(x + 1, y)
            i1 = getnum(x - 1, y - 1)
            i2 = getnum(x, y - 1)
            i3 = getnum(x + 1, y - 1)
            j1 = getnum(x - 1, y + 1)
            j2 = getnum(x, y + 1)
            j3 = getnum(x + 1, y + 1)
            if i2 is not None: 
                i1 = None
                i3 = None
            if j2 is not None: 
                j1 = None
                j3 = None
            a = [left, right, i1, i2, i3, j1, j2, j3]
            print(a)
            a = list(aa for aa in a if aa is not None)
            if len(a) == 2:
                total2 += a[0] * a[1]
print(total2)