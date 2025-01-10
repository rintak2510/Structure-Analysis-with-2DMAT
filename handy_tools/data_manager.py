# 使用上の注意
# 事前にpandas, numpyはインストールしておかないと動作しません。
# 本プログラムと同一のディレクトリに各測定データの親ディレクトリとcsvファイルが入るようにしてください。

# 実験データのディレクトリでディレクトリを検索する。
# 'result of intensity.txt'が存在するかどうか確認する。
# 存在するのであれば'result of intensity.txt'をコピーし、保存名をoriginに使っている短縮名に変更する。
# 短縮名に変更されたファイルはサンプル名がついたディレクトリに格納する。
# 操作の完了したディレクトリは'YYYYMMDD-HHMMSS.bak'という名称に変更する。

# 下準備：タイムスタンプ、ショートネーム、サンプル名、入射方向をまとめたテーブルを作成する

import subprocess
import os
import pandas as pd
import stdutils

# まずはpandasでテーブルを読み込む
data_manager = pd.read_csv('data_manager.csv')

# 保存先のフォルダを作っておかなければならないため
for sample in data_manager['sample'].unique():
    os.makedirs(sample, exist_ok=True)
    os.chdir(sample)
    child_dirs = data_manager.query('sample.str.match(@sample)')['direction'].unique()
    for child_dir in child_dirs:
        os.makedirs(child_dir,exist_ok=True)
    os.chdir('../')

# ディレクトリを順次読み込んで、処理を行えるようにする
tmp = subprocess.check_output('ls -F | grep /', shell=True, text=True)
dirs = tmp.strip().split('\n')

for d in dirs:
    target_file = d + 'result of intensity.txt'
    
    if os.path.exists(target_file):
        # 先に保存箇所やショートネームを取得しなくてはならない。
        information = data_manager.query('timestamp == @d')

        # 面倒でやらなかったが本来はここでdata_managerのデータ照合に失敗した時のエラーを処理する必要がある
        name, sample, direction = information.iloc[0][1:4]
        destination = sample + '/' + direction + '/' + name + '.txt'
        subprocess.run(['cp', target_file, destination])

        # 処理が完了したことを示せるように、成功メッセージを返し、保存形式を変更する
        print('Saving' + d + 'succeeded.')
        new_name = d[:-1] + '.bak'
        os.rename(d, new_name)

    # それ以外の場合は保存の失敗したことを返すようにする。
    else:
        print('SAVING' + d + 'FAILED!')

        
