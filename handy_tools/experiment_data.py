import os
import pandas as pd
import matplotlib.pyplot as plt

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
os.system('open experiment.png')
