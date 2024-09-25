input_file = input()   # 読み込み元のファイル名
output_file = input()  # 書き込み先のファイル名

def sort_lines_by_last_value(input_file, output_file):
    # ファイルを読み込み
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # 各行を最後の値でソートする
    # まず行ごとに最後の値でソートできるように変換
    sorted_lines = sorted(lines, key=lambda line: float(line.split()[-1]))
    
    # ソートされた行を新しいファイルに書き込む
    with open(output_file, 'w') as file:
        file.writelines(sorted_lines)

sort_lines_by_last_value(input_file, output_file)
