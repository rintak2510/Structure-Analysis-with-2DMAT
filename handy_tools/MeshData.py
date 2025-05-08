import numpy as np
from itertools import product

# 軸ごとに不等間隔に設定も可能
z1 = np.linspace(3.6, 4.0, 5)
z2 = np.linspace(3.6, 4.0, 5)
z3 = np.linspace(3.4, 3.8, 3)

points = list(product(z1, z2, z3))

with open("meshdata.txt", "w") as f:
    for p in points:
        f.write(" ".join(map(str, p)) + "\n")
