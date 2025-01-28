import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from decimal import *
import re
import math

# 本プログラムは構造を周期的に繰り返し、緩和させるプログラムである。
# surf_temp.txtで構造以外のパラメターを指定し、残りはデータをもとに再起的に作成する

# とりあえずパラメターを設定させる
period = 9
unit_len = 4.01245

R = 3.00
r = 0.02
z1 = 2.8
z2 = 2.7
z_bulk = 3.276
z0 = 0.80
sic = 0.005

# 上記から計算される必要パラメター
R0 = unit_len / math.sqrt(3)
R_ratio = ( R - R0 ) / R0
z0 += z_bulk
z1 += z0
z2 += z0


# 読み込むファイル一覧
surf_file = 'surf_temp.txt'
tmp0 = pd.read_csv('str_param_org.csv')

# 出力ファイル名
output_file = 'surf.txt'

# 単位構造を触るプログラム

# T1サイトPb原子を上から順に一つずつ置換していく
tmp0.iloc[0,2] = ( 1 + R_ratio ) / 3
tmp0.iloc[0,3] = 2 * ( 1 + R_ratio ) / 3
tmp0.iloc[0,4] = z1
tmp0.iloc[1,2] = 2 * ( 2 - R_ratio ) / 3
tmp0.iloc[1,3] = ( 2 - R_ratio ) / 3
tmp0.iloc[1,4] = z1
tmp0.iloc[2,2] = ( R_ratio - 2 ) / 3
tmp0.iloc[2,3] = ( 2 - R_ratio ) / 3
tmp0.iloc[2,4] = z1
tmp0.iloc[3,4] = z2

# 緩和したGe原子を上から順に一つずつ置換していく
tmp0.iloc[4,2] = 4 * ( 1 + r ) / 3
tmp0.iloc[4,3] = 2 * ( 1 + r ) / 3
tmp0.iloc[4,4] = z0
tmp0.iloc[5,2] = ( 1 + r ) / 3
tmp0.iloc[5,3] = - ( 1 + r ) / 3
tmp0.iloc[5,4] = z0
tmp0.iloc[6,2] = ( 1 + r ) / 3
tmp0.iloc[6,3] = 2 * ( 1 + r ) / 3
tmp0.iloc[6,4] = z0

tmp1 = tmp0.copy()

# 構造を作成する部分。周期の分だけ構造を繰り返す
for i in range(1,period):
    tmp1['a1'] = tmp1['a1'].apply( lambda x: x + 2 )
    tmp1['a2'] = tmp1['a2'].apply( lambda x: x + 1 )
    tmp2 = pd.concat([tmp0, tmp1], ignore_index=True)
    tmp0 = tmp2.copy()

# Dは(-1,1)からの距離、dは(2,1)からの距離を指定する物である
# 各単位ベクトルをもとに規格化している

tmp2['D'] = tmp2[['a1', 'a2']].apply( lambda x: \
        abs( x.iloc[0] + x.iloc[1] ) / 3, axis=1 )
tmp2['d'] = tmp2[['a1', 'a2']].apply( lambda x: \
        abs( x.iloc[0] / 2 - x.iloc[1] ) * 2 / 3, axis=1 )

# 基板からの距離に比例して凸凹するようにする
# 最も基板から離れた原子を1として規格化する

z_max = tmp2['z'].max()
tmp2['diff'] = tmp2[['z', 'D']].apply( lambda x: \
        x.iloc[0] * sic  / z_max * ( ( x.iloc[1] - period / 2 ) ** 2 - period ** 2 / 4 ), axis=1 )

# パラメターを順次整形していく

tmp2['D'] = tmp2[['D', 'diff']].apply( lambda x: x.iloc[0] + x.iloc[1], axis=1 )
tmp2['a1'] = tmp2[['D', 'd']].apply( lambda x: format( x.iloc[0] * 2 - x.iloc[1], '.5f' ), axis=1 )
tmp2['a2'] = tmp2[['D', 'd']].apply( lambda x: format( x.iloc[0] + x.iloc[1], '.5f'), axis=1 )
tmp2['density'] = tmp2['density'].apply( lambda x: format(x, '.2f') )
tmp2['z'] = tmp2['z'].apply( lambda x: format(x, '.4f') )

structure = tmp2[['atom', 'density', 'a1', 'a2', 'z']]

with open(surf_file, 'r') as file:
    surf_lines = file.readlines()

atom_type = int(surf_lines[0])
atom_param = surf_lines[:(atom_type * 2 + 1)]
basic_param = [surf_lines[(atom_type * 2 + 1)]]
basic_param = basic_param[0].split(',')
basic_param[1] = str( int(basic_param[1]) * period )
basic_param[2] = str( int(basic_param[2]) * period )
basic_param = [','.join(basic_param)]

structure_lines = structure.to_csv(index=False, header=False).splitlines()
atoms = [f"{len(structure_lines)}\n"]
structure_param = []

for line in structure_lines:
    parts = re.split(r',', line.strip())
    formatted_line = ', '.join(parts)
    structure_param.append(formatted_line + '\n')

result = atom_param + basic_param + atoms + structure_param + ['1']

with open(output_file, 'w') as file:
    file.writelines(result)

