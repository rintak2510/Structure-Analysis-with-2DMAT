import pandas as pd

output_file = "rz_dependency.txt"
param_name = {1: 'r1', 2: 'r2', 3: 'z1', 4: 'z2', 10: "R"} # 辞書型で与える

df_res = pd.read_csv("ColorMap.txt", sep="\s+", header=None)
df_params= pd.read_csv("ParamsList.txt", sep="\s+", header=None).drop(0,axis=1)
df_out = df_params.join(df_res.iloc[:, -1]).rename(columns=param_name)
df_out.to_csv(output_file, sep="\t", index=False)
