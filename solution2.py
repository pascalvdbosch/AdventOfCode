with open('input2.txt', 'r') as i:
    games = [game.strip() for game in i.readlines()]

bag = [12, 13, 14]

def u(sp):
    ret = [None, None, None]
    for s in sp:
        for i, col in enumerate(["red", "green", "blue"]):
            if col in s:
                ret[i] = int(s.replace(col, "").strip())
    return ret

id = 0
total = 0
total2 = 0
for game in games:
    id += 1
    game = [u(sp.split(",")) for sp in game[game.index(":") + 2:].split(";")]
    if all(all(g <= b for g, b in zip(grab, bag) if g is not None) for grab in game): total += id
    r, g, b = [max(grab[i] for grab in game if grab[i] is not None) for i in [0, 1, 2]]
    total2 += r * g * b
print(total)
print(total2)