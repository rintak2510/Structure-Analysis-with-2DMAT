import matplotlib.pyplot as plt
import numpy as np
import glob
import re
import os
import subprocess
import platform

dir_name = 'calculations'
experiment_file = "experiment.txt"
con_file_pattern = "con(*,*,*).txt"

def normalize_and_plot_specific_files(dir_name, experiment_file, con_file_pattern):
    plt.figure( figsize=(15, 10), \
                # facecolor='ivory' \
               )

    # 実験結果のRCを用意するところ
    try:
        data = np.loadtxt(experiment_file)
        x = data[:, 0]
        y = data[:, 1]
        y_normalized = y / np.max(y)
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
    os.chdir(dir_name)
    con_files = glob.glob(con_file_pattern) # マッチするパスを全て回収
    valid_con_files = []
    
    for file in con_files:
        if re.match(r"con\(\d+\.\d+,\d+\.\d+,\d+\.\d+\)\.txt", file):
            valid_con_files.append(file)
    
    if not valid_con_files:
        print("No valid con(R,r,SIC) files found.")
        return

    # ファイル処理部分
    for file in valid_con_files:
        try:
            data = np.loadtxt(file)
            x = data[:, 0]
            y = data[:, 1]
            y_normalized = y / np.max(y)
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

    os.rename('Compare_RC.png', '../Compare_RC.png')
    os.chdir('../')
    open_img('Compare_RC.png')

def open_img(image_path):
    if platform.system() == "Windows":
        os.startfile(image_path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", image_path])
    else:  # Linux
        subprocess.run(["xdg-open", image_path])

normalize_and_plot_specific_files(dir_name, experiment_file, con_file_pattern)
