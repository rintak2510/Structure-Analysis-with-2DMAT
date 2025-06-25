import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess
import platform

filename = '100.txt'
savename = ''

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

def open_img(image_path):
    if platform.system() == "Windows":
        os.startfile(image_path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", image_path])
    else:  # Linux
        subprocess.run(["xdg-open", image_path])

def heatmap_generator(savename, data):
    savename = filename[:-3] + 'png' if savename == '' else savename
    fig, ax = plt.subplots()
    cax = ax.imshow(data, cmap='inferno', aspect='auto')
    fig.colorbar(cax, ax=ax, label='Intensity')
    plt.savefig(savename)
    open_img(savename)

data = intensity_data(filename)
heatmap_generator(savename, data)
