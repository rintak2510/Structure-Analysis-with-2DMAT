from itertools import product
import numpy as np

# パラメータ空間の各軸
a1_vals = np.linspace(-0.3, -0.2, 101)
z1_vals = np.linspace(13.1, 13.5, 21)
a0_vals = np.linspace(-0.31, -0.28, 31)
z0_vals = np.linspace(10.4, 10.8, 9)

# 出力ファイルに逐次書き出し
with open("MeshData.txt", "w") as f:
    idx = 0
    for a1, z1, a0, z0 in product(a1_vals, z1_vals, a0_vals, z0_vals):
        # 制約条件が必要な場合はここに記述（例: z1 > z0）
        if z1 > z0:
            line = [a1, -a1, z1, a0, -a0, z0]
            f.write(f"{idx} " + " ".join(map(str, line)) + "\n")
            idx += 1
