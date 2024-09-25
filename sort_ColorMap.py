import NumPy as np

fxlist = []
combined = []

files_input = open("ColorMap.txt","r")
lines = files_input.readlines()

for line in lines:
    if line[0] != "#":
        combined.append(line)
        data = line.split()
        fx = data[-1]
        fxlist.append(float)

combined.sort(key=operator.itemgetter(-1),reverse=True)

output = open("sorted_ColorMap.txt","w+")
for nums in combined:
    output.writelines(nums)
output.close
