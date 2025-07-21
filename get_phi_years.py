import math

N0 = 1.448e24
N_max = 1.74e64
phi = (1 + math.sqrt(5)) / 2
t = math.log(N_max / N0) / math.log(phi)
print(int(2025 + t)) 