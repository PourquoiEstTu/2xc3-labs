from itertools import combinations

l = [0,1,2,3]

comb = combinations(l, 2)

comb3 = combinations(comb, 4)

print(l)

print(list(comb))

print(list(comb3))
