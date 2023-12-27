with open('input4.txt', 'r') as i:
    data = [[[int(s.strip()) for s in sp.split(",")] for sp in line.split("@")] for line in i.readlines()]
N = len(data)

xmin = 7
xmax = 27
ymin = 7
ymax = 27
xmin = 200000000000000
xmax = 400000000000000
ymin = 200000000000000
ymax = 400000000000000

def when(x, y, dx, dy, x0, y0):
    x0 -= x
    y0 -= y
    inwendig = dx * x0 + dy * y0
    return inwendig

# part I
hit = 0
for p1 in range(N):
    for p2 in range(N):
        if p1 <= p2: continue
        # print("Hailstone A: " + str(data[p1]))
        # print("Hailstone B: " + str(data[p2]))
        [xyz1, uvw1] = data[p1]
        [xyz2, uvw2] = data[p2]
        x1 = xyz1[0]
        y1 = xyz1[1]
        x2 = xyz2[0]
        y2 = xyz2[1]
        if uvw1[0] == 0:
            if uvw2[0] == 0:
                x, y = None, None # parallel
                # print("parallel")
            else:
                dydx2 = uvw2[1] / uvw2[0]
                if ((uvw2[0] > 0 and x1 > x2) or 
                    (uvw2[0] < 0 and x1 < x2)): 
                    y = y2 + (x1 - x2) * dydx2
                    x = x1
                else:
                    x, y = None, None # history
                    # print("history")
        else:
            if uvw2[0] == 0:
                dydx1 = uvw1[1] / uvw1[0]
                y = y1 + (x2 - x1) * dydx1
                x = x2
                if ((uvw1[0] > 0 and x2 > x1) or 
                    (uvw1[0] < 0 and x2 < x1)): 
                    y = y1 + (x2 - x1) * dydx1
                    x = x2
                else:
                    x, y = None, None # history
                    # print("history")
            else:
                dydx1 = uvw1[1] / uvw1[0]
                dydx2 = uvw2[1] / uvw2[0]
                # y1 + dydx1 * (x - x1)
                # (y1 - dydx1 * x1) + (dydx1) * x
                a = dydx1 # a
                c = y1 - dydx1 * x1 # c
                b = dydx2 # b
                if a == b:
                    x, y = None, None # parallel
                    # print("parallel")
                else:
                    d = y2 - dydx2 * x2 # d
                    x = (d - c) / (a - b)
                    y = a * (d - c) / (a - b) + c
                    if when(x1, y1, uvw1[0], uvw1[1], x, y) < 0 or when(x2, y2, uvw2[0], uvw2[1], x, y) < 0:
                        x, y = None, None # history
                        # print("history")
        if x is not None:
            if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
                # print(x, y)
                hit += 1
            else:
                pass # print("outside")

print("Solution: ", hit)

# Part II

# x0_ + xv_ * t[i] = x0[i] + xv[i] * t[i]
# y0_ + yv_ * t[i] = y0[i] + yv[i] * t[i]
# z0_ + zv_ * t[i] = z0[i] + zv[i] * t[i]
# solve for: x0_, y0_, z0_, xv_, yv_, zv_, t[i] for all i. That is in total 6 + N unkowns, and 3 * N equations

from scipy.optimize import fsolve, root
import random

def equations(vars):
    xyz0_ = vars[0:3]
    uvw_ = vars[3:6]
    t = vars[6:]
    return list(j for i in range(N) for j in [xyz0_[dim] + uvw_[dim] * t[i] - data[i][0][dim] + data[i][1][dim] * t[i] for dim in [0, 1, 2]])

initial_guess = list(xmin + (xmax - xmin) * random.random() for i in range(3)) + list(1 for i in range(3)) + list(random.random() * 100000 for i in range(N))
solution = root(equations, initial_guess, method='lm')
print("Solution:", sum(solution.x[:3]))