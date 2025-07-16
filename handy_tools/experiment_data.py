import os
import pandas as pd
import matplotlib.pyplot as plt
import platform
import subprocess

dataset = pd.read_csv('112_Data.csv')

angles = dataset["Angle"]
plt.figure(figsize=(8, 6))
for column in dataset.columns[1:]:
    plt.plot(angles, dataset[column], marker='o', label=column)

plt.xlabel("Incident Angle (°)")
plt.ylabel("Intensity (abs.unit)")
plt.title("Bi/Ge(111)")
plt.legend(title="Data Sets")
plt.grid(True)
plt.tight_layout()
plt.savefig('experiment.png')
open_img('experiment.png')

def open_img(image_path):
    if platform.system() == "Windows":
        os.startfile(image_path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", image_path])
    elif "microsoft" in platform.release().lower():  # for WSL
        subprocess.run(["explorer.exe", image_path])
    else:  # Linux
        subprocess.run(["xdg-open", image_path])
