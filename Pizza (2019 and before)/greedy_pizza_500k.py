# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 11:13:48 2019

@author: Giulia C
"""

pizza = []
sol = []
input()

r,c,l,h = 1000, 1000, 6, 14
a,b = 1,14

for i in range(0, r):
    pizza.append(list(input()))

def valid(sl,start):
    tom = 0
    mush = 0
    for row in sl:
        for element in range(j,j+b):
            if row[element] == "T":
                tom += 1
            else:
                mush += 1
    return (tom >= l and mush >= l)

i = 0

while i < r-a:
    j=0
    while j < c-b:
        if (valid(pizza[i:i+a],j)):
            sol.append([i,j,i+a-1,j+b-1])
        j += b
    i += a
    
print(len(sol))
for sl in sol:
    print(sl[0],sl[1],sl[2],sl[3])

        
                