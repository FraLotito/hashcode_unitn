"""
Francesco Lotito
lotitoqf@gmail.com

esempio: 15
small: 42
medium: 49395
big: 894249
"""

from __future__ import print_function
import sys
import random

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

R, C, L, H = list(map(int, input().split()))

def rettangoli(H):
    res = set()
    for i in range(1, H+1):
        for j in range(1, H+1):
            if i*j <= H:
                res.add((i,j))
    return res

def ordina(rett):
    # euristiche
    #return list(sorted(list(rett), key = lambda x: x[1], reverse=False))
    #return list(sorted(list(rett), key = lambda x: x[0], reverse=True))

    # DECOMMENTA PER MEDIUM E BIG
    return list(sorted(list(rett), key = lambda x: x[1], reverse=True))
    
    #return list(sorted(list(rett), key = lambda x: x[0]*x[1], reverse=True))
    #return list(sorted(list(rett), key = lambda x: x[0]*x[1], reverse=False))
    #return list(sorted(list(rett), key = lambda x: x[0], reverse=False))

pizza = []
for _ in range(R):
    pizza.append(input())

rett = ordina(rettangoli(H))
def set_used(a,b,c,d):
    for i in range(a, b+1):
        for j in range(c, d+1):
            used[i][j] = True

# TRUE PER ESEMPIO E SMALL
random_enabled = False

if random_enabled:
    N_iter = 1000
else:
    N_iter = 1

max_area = 0
sol = []

for _ in range(N_iter):
    used = []
    for _ in range(R):
        used.append([False] * C)
    slices = []
    area = 0

    for i in range(R):
        for j in range(C):
            if random_enabled:
                random.shuffle(rett)
            if not used[i][j]:
                # provo ad inserire i rettangoli e prendo il primo valido
                for r in rett:
                    if i + r[0] - 1 < R and j + r[1] - 1 < C:
                        ok = True
                        t = 0
                        f = 0
                        for z in range(i, i+r[0]):
                            t = t + pizza[z][j:j+r[1]].count('T')
                            f = f + pizza[z][j:j+r[1]].count('M')
                            if True in used[z][j:j+r[1]]:
                                # non posso prenderlo
                                ok = False
                                break

                        if ok and t >= L and f >= L:
                            # posso prenderlo
                            set_used(i, i+r[0]-1, j, j+r[1]-1)
                            slices.append((i, i+r[0]-1, j, j+r[1]-1))
                            area += (r[0]*r[1])
                            break
    eprint(area)
    if area > max_area:
        max_area = area
        sol = slices.copy()

    # ogni tot iterazioni sarebbe cosa buona fare un dump della soluzione trovata fino a quel momento

print(len(sol))
for i in sol:
    out = str(i[0]) + ' ' + str(i[2]) + ' ' + str(i[1]) + ' ' + str(i[3])
    print(out)

eprint(max_area)