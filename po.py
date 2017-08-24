import math

print('[', end='')
for t in range(500):
    print('[{}, {}],'.format(t, 50 * math.sin(3 * t / 30 + 10)), end='')
print(']', end='')
