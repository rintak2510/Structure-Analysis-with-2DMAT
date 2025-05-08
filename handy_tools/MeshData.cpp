from mpi4py import MPI
import numpy as np
import os

# MPI初期化
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# パラメータ空間の各軸
z1 = np.linspace(3.2, 4.0, 9)
z2 = np.linspace(3.2, 4.0, 9)
z3 = np.linspace(3.2, 4.0, 9)
z4 = np.linspace(3.2, 4.0, 9)
a1 = np.linspace(0.40, 0.50, 21)
a2 = np.linspace(1.20, 1.30, 21)
a3 = np.linspace(0.40, 0.50, 21)
a4 = np.linspace(1.20, 1.30, 21)
b1 = np.linspace(1.55, 1.65, 21)
b2 = np.linspace(0.70, 0.80, 21)
b3 = np.linspace(0.70, 0.80, 21)
b4 = np.linspace(1.55, 1.65, 21)

axes = [z1, z2, z3, z4, a1, a2, a3, a4, b1, b2, b3, b4]
shape = list(map(len, axes))  # 各軸の長さ
total_points = np.prod(shape)  # 全体の組み合わせ数

# インデックスから多次元インデックスに変換
def unravel_index(idx, shape):
    indices = []
    for s in reversed(shape):
        indices.append(idx % s)
        idx //= s
    return list(reversed(indices))

# 出力ファイル（ランク別）
output_file = f"MeshData_rank{rank}.txt"

with open(output_file, "w") as f:
    for flat_idx in range(rank, total_points, size):
        multi_idx = unravel_index(flat_idx, shape)
        values = [axes[dim][i] for dim, i in enumerate(multi_idx)]
        line = f"{flat_idx + 1} " + " ".join(map(str, values)) + "\n"
        f.write(line)

if rank == 0:
    print(f"[INFO] 出力完了: 各ランク {output_file} に書き出しました（全 {total_points:,} 点）")

