from itertools import product
import numpy as np

# パラメータ空間の各軸
r1_max = 2.31659
r2_max = 2.00622
# r1, z1はPb
# r2, z2はBi
z_0 = 0.82704

r1_vals = np.linspace(0.3, 1.5, 25)
r2_vals = np.linspace(0.3, 1.5, 25)
z1_vals = np.linspace(2.6, 3.8, 25)
z2_vals = np.linspace(2.6, 3.8, 25)

# 出力ファイルに逐次書き出し
with open("ParamsList.txt", "w") as f:
    idx = 0
    for r1, r2, z1, z2 in product(r1_vals, r2_vals, z1_vals, z2_vals):
        # r1方向 (a,b)=(1,-1)/3
        # r2方向 (a,b)=(1,1)/3
        # a1 = 5/3 - r1 / r1_max / 3
        # b1 = 1/3 + r1 / r1_max / 3
        # a2 = 2/3 + r1 / r1_max / 3
        # b2 = 4/3 - r1 / r1_max / 3
        # a3 = 2/3 + r2 / r2_max / 3
        # b3 = 1/3 + r2 / r2_max / 3
        # a4 = 5/3 - r2 / r2_max / 3
        # b4 = 4/3 - r2 / r2_max / 3
        # z1 = z1 + z_0
        # z2 = z2 + z_0

        # 変数の定義
        # line = [a1, b1, a2, b2, a3, b3, a4, b4, z1, z2]
        line = [r1, r2, z1, z2]
        f.write(f"{idx} " + " ".join(map(str, line)) + "\n")
        idx += 1

        # 制約条件が必要な場合はここに記述（例: z1 > z0）
#         if z1 > z0:
#             line = [a1, -a1, z1, a0, -a0, z0]
#             f.write(f"{idx} " + " ".join(map(str, line)) + "\n")
#             idx += 1
