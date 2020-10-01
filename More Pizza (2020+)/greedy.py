import sys


fname = sys.argv[1]
print("Reading input file:", fname)
with open(fname) as f:
    M, N = map(int, f.readline().split())
    slices_raw = map(int, f.readline().split())

slices_map = []
for i, s in enumerate(slices_raw):
    slices_map.append((i, s))

slices_map.sort(key=lambda x: x[1])

slices_so_far = 0
solution = []
while slices_so_far < M and len(slices_map) > 0:
    next = slices_map.pop()
    if slices_so_far + next[1] <= M:
        slices_so_far += next[1]
        solution.append(next[0])

print("Slices:", slices_so_far)
# print("Solution:", solution)
