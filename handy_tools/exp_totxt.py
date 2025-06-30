import pandas as pd
import sys
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

filename = sys.argv[1]
row = 'intensity3'

def open_data(filename, row):
    with open (filename, 'r') as file:
        lines = file.readlines()
        file.close()

    data_list = []
    for i in lines:
        i = i.replace('\n', '').split('\t')
        data_list.append(i)

    df_data = pd.DataFrame(data_list[1:], columns=data_list[0]).astype(float)
    exp = df_data[['Angle', row]]
    exp[row] = exp[row] / exp[row].sum()
    return exp

def show_image(df):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(6, 4))
    plt.scatter(df['Angle'], df[row],
                edgecolor='Red', \
                facecolor='None', \
                s=200, \
                linewidth=2.0 
                )
    plt.xlabel('Angle')
    plt.ylabel(row)
    plt.title('Experiment Data')
    plt.show()

def export_to_txt(filename, exp):
    exp_list = exp.values.tolist()
    lines = []
    
    for i in exp_list:
        i = '\t'.join(map(str, i)) + '\n'
        lines.append(i)
    
    with open('experiment.txt', 'w') as file:
        file.writelines(lines)
        file.close()
    
    print(f"Exported {filename} successfully.")
    
df = open_data(filename, row)
export_to_txt(filename, df)
show_image(df)
