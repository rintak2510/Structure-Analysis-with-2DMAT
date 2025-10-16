# 要件：計算のための形式と実際の変数空間の形式が異なるため、計算結果を変数空間に統合する

import pandas as pd

params_filepath = "ParamsList.txt"
results_filepath = "ColorMap.txt"
output_filepath = "rz_dependency.txt"

df_params = pd.read_csv(params_filepath, sep=r"+\s", header=None).drop(0,axis=1)
df_res = pd.read_csv(results_filepath, sep=r"\s+", header=None)
df = df_params.join(df_res[10])
df = df.rename(columns={1:'r1',2:'r2',3:'z1',4:'z2',10:'R'})

df.to_csv(output_filepath, sep='\t',index=False)
