import matplotlib.pyplot as plt
import numpy as np
import glob
import re

def normalize_and_plot_specific_files(experiment_file, con_file_pattern):
    """
    Normalize and plot data from a specified experiment file and con(R,r) pattern files.

    Args:
        experiment_file (str): Path to the experiment file (e.g., "experiment.txt").
        con_file_pattern (str): Pattern for con(R,r) files (e.g., "con(*,*).txt").
    """
    # Initialize the plot
    plt.figure(figsize=(10, 6))
    
    # Process the experiment file
    try:
        data = np.loadtxt(experiment_file)
        x = data[:, 0]
        y = data[:, 1]
        y_normalized = y / np.max(y)
        plt.plot(x, y_normalized, label=f"Experiment: {experiment_file}", linestyle='--')
    except Exception as e:
        print(f"Error processing experiment file '{experiment_file}': {e}")
    
    # Process con(R,r) files
    con_files = glob.glob(con_file_pattern)
    valid_con_files = []
    
    for file in con_files:
        # Match the con(R,r) pattern using a regex
        if re.match(r"con\(\d+\.\d+,\d+\.\d+\)\.txt", file):
            valid_con_files.append(file)
    
    if not valid_con_files:
        print("No valid con(R,r) files found.")
        return

    # Plot con(R,r) files
    for file in valid_con_files:
        try:
            data = np.loadtxt(file)
            x = data[:, 0]
            y = data[:, 1]
            y_normalized = y / np.max(y)
            plt.plot(x, y_normalized, label=f"Con File: {file}")
        except Exception as e:
            print(f"Error processing file '{file}': {e}")
    
    # Customize the plot
    plt.xlabel("X-axis")
    plt.ylabel("Normalized Y-axis")
    plt.title("Normalized Data from Experiment and Con Files")
    plt.legend(loc="best")
    plt.grid(True)
    plt.tight_layout()
    
    # Show the plot
    plt.savefig('Compare_RC.png')

# Example usage
experiment_file = "experiment.txt"            # Path to the experiment file
con_file_pattern = "con(*,*).txt"             # Glob pattern for con(R,r) files
normalize_and_plot_specific_files(experiment_file, con_file_pattern)
