import pandas as pd

with open('experiment.txt', 'r') as f:
    exp_lines = f.readlines()
    f.close()            
         
with open('angle_rot/con_-30.txt', 'r') as f:
     calc_lines = f.readlines()
     f.close()

exp_list = []
calc_list = []

for i in exp_lines:
     i = i.replace('\n','').split('\t')
     exp_list.append(i)

for i in calc_lines:
     i = i.replace('\n','').split(' ')
     calc_list.append(i)

df_calc = pd.DataFrame(calc_list,columns=['Angle', 'Calc']).astype(float)
df_exp = pd.DataFrame(exp_list, columns=['Angle', 'Exp']).astype(float)

data = pd.merge(df_exp, df_calc, on='Angle')

data['Exp'] = data['Exp'] / data['Exp'].sum()
data['Calc'] = data['Calc'] / data['Calc'].sum()

out = data.to_csv('defined.txt',header=False, index=False)
