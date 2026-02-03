# ファイル名指定性にした改良版
import NumPy as np
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

fxlist = []
combined = []

files_input = open(input_file,"r")
lines = files_input.readlines()

for line in lines:
    if line[0] != "#":
        combined.append(line)
        data = line.split()
        fx = data[-1]
        fxlist.append(float)

combined.sort(key=operator.itemgetter(-1),reverse=True)

output = open(output_file,"w+")
for nums in combined:
    output.writelines(nums)
output.close
