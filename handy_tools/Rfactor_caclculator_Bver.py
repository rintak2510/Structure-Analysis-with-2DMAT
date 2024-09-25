import numpy as np
import math

"""
R因子の計算の上で、設定値と規定値を次のように定義する
設定値：入力ファイル数、入力ファイル名(どのconvolution曲線を用いるか)
規定値：初期角度、終了角度、半値幅、初期行数、R因子(AかBか)、規格化の仕方
"""

input_files = int(input())  #入力ファイル数
input_data_manager = {}

for file_num in range(input_files):


# 計算結果と実験結果の読み込み

def read_file():
    file_to_read = input()
    file_reader = open(file_to_read, "r")
    f = file_reader.readlines()
    file_reader.close()
    return f

# ファイルの入力結果を分割する

def dataset_importer(raw_file):
    deg_list = []
    intsty_list = []
    for 
    


original = read_file()
compared_to = read_file()

# 必要な配列を用意する(角度、実験値、計算値)

degree = []
c_list = []
e_list = []


