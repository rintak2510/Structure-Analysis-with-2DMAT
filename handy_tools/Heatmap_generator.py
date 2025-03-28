import numpy as np
import matplotlib.pyplot as plt
import os

filename = '100.txt'
#savename = 

def intensity_data(filename):
    with open(filename, 'r') as f:
        origin = f.readlines()
        f.close()

    data = []

    for i in origin:
        i = i.replace('\n', '').split('\t')
        data.append(i)

    data = np.array(data).astype(int)
    return data

try:
    savename
except:
    savename = filename[:-3] + 'png'

data = intensity_data(filename)
fig, ax = plt.subplots()
img = ax.imshow(data)
plt.savefig(savename)
os.system('open ' + savename)
