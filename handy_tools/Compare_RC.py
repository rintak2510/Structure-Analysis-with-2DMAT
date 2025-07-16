import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import subprocess
import platform
import pandas as pd

experiment_file = "experiment.txt"
con_file_pattern = "con_*.txt"

def normalize_and_plot_specific_files(experiment_file, con_file_pattern):
    plt.figure( figsize=(15, 10), \
                # facecolor='ivory' \
               )

    # 実験結果のRCを用意するところ
    try:
        data = np.loadtxt(experiment_file)
        x = data[:, 0]
        y = data[:, 1]
        y_normalized = y / np.sum(y)
        plt.scatter(    x, y_normalized, \
                        label=f"Experiment: {experiment_file}", \
                        edgecolor='Red', \
                        facecolor='None', \
                        s=500, \
                        linewidth=2.0 \
                    )
    except Exception as e:
        print(f"Error processing experiment file '{experiment_file}': {e}")
    
    # 計算結果のRCを用意するところ
    con_files = glob.glob(con_file_pattern) # マッチするパスを全て回収
    valid_con_files = []
    
    for file in con_files:
        valid_con_files.append(file)
    
    if not valid_con_files:
        print("No matched files found.")
        return

    # ファイル処理部分
    for file in valid_con_files:
        try:
            data = np.loadtxt(file)
            x = data[:, 0]
            y = data[:, 1]
            y_normalized = y / np.sum(y)
            plt.plot( \
                    x, y_normalized, \
                    label=f"Con File: {file}" 
                        )
        except Exception as e:
            print(f"Error processing file '{file}': {e}")
    
    # 画像作成部分
    plt.xticks( fontsize=28, \
                fontname="Times New Roman")
    plt.gca().tick_params( \
                axis="x", \
                direction="in", \
                width=1, \
                length=10, \
                pad=14 )
    plt.yticks([])
    plt.xlabel("Glancing angle (degree)", \
                labelpad=18, \
                fontsize=32, \
                fontname="Times New Roman")
    plt.ylabel("Intensity (abs. unit)", \
                labelpad=22, \
                fontsize=32, \
                fontname="Times New Roman")
    plt.legend( loc="best", \
                fontsize=20 )
    plt.tight_layout()
    plt.savefig('Compare_RC.png')
    open_img('Compare_RC.png')

def open_img(image_path):
    if platform.system() == "Windows":
        os.startfile(image_path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", image_path])
    elif "microsoft" in platform.release().lower():  # for WSL
        subprocess.run(["explorer.exe", image_path])
    else:  # Linux
        subprocess.run(["xdg-open", image_path])


def refine_to_dft(experiment_file, con_file_pattern):
    try:
        with open(experiment_file, 'r') as f:
            exp_line = f.readlines()
            f.close()

        exp_data = []
        for i in exp_line:
            i = i.replace('\n','').split('\t')
            exp_data.append(i)

        df_exp = pd.DataFrame(exp_data).astype(float).rename(columns={0:'Angle', 1:'Exp'})
        df_exp['Exp'] = df_exp['Exp'] / df_exp['Exp'].sum()

    except Exception as e:
        print(f"Error processing experiment file '{experiment_file}': {e}")
    
    # 計算結果のRCを用意するところ
    con_files = glob.glob(con_file_pattern) # マッチするパスを全て回収
    valid_con_files = []
    
    for file in con_files:
        valid_con_files.append(file)
    
    if not valid_con_files:
        print("No matched files found.")
        return

    # ファイル処理部分
    try:
        df = df_exp
        for idx, file in enumerate(valid_con_files):
            with open(file, 'r') as f:
                calc_line = f.readlines()
                f.close()

            calc_data = []

            for i in calc_line:
                i = i.replace('\n','').split()
                calc_data.append(i)

            name = 'Calc' + str(idx+1)
            df_calc = pd.DataFrame(calc_data).astype(float).rename(columns={0: 'Angle',1: name})
            df_calc[name] = df_calc[name] / df_calc[name].sum()
            df = df.merge(df_calc, how='left', on='Angle')
        df.to_csv('Data.csv',header=False,index=False)

    except Exception as e:
        print(f"Error processing file '{file}': {e}")
        
normalize_and_plot_specific_files(experiment_file, con_file_pattern)
refine_to_dft(experiment_file, con_file_pattern)
