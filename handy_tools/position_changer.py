import re
import subprocess


def modify_surf_file_preserve_spacing(file_path, output_path, percentage1, percentage2):
    
    # Define A and B
    A = (-0.6666667, 0.6666667)
    B = (-0.3333333, 0.3333333)
    
    # Calculate new values for each percentage
    new_X = A[0] + percentage1 * (B[0] - A[0])
    new_Y = A[1] + percentage1 * (B[1] - A[1])
    new_x = A[0] + percentage2 * (B[0] - A[0])
    new_y = A[1] + percentage2 * (B[1] - A[1])
    
    # Helper function to preserve spacing
    def modify_line(line, new_values):
        # Split the line using regex to keep separators (spaces or tabs)
        parts = re.split(r'(\s+)', line)
        # Update the 3rd and 4th numeric values (index 4 and 6 due to separators)
        parts[4] = f"{new_values[0]:.5f}"
        parts[6] = f"{new_values[1]:.5f}"
        return ''.join(parts)

    # Read the input file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Modify the 10th and 12th lines
    lines[9] = modify_line(lines[9], (new_X, new_Y))
    lines[11] = modify_line(lines[11], (new_x, new_y))
    
    # Write the modified lines to the output file
    with open(output_path, 'w') as file:
        file.writelines(lines)

# changing the default to real length
given = input().split(', ')
R = float(given[0])
r = float(given[1])
a = 2.31659                     # In-plane distance to T1 site

percentage1 = (R-a)/a           # 50% movement from A to B
percentage2 = r/a               # 30% movement from A to B

# Example usage
input_file = "surf_org.txt"      # Path to your surf.txt
output_file = "surf.txt"         # Path to save the modified file

modify_surf_file_preserve_spacing(input_file, output_file, percentage1, percentage2)

filename = 'con' + '\(' + given[0] + ',' + given[1] + '\)' + '.txt'

# give the filename by using subprocess module to input, which is 'read' in shell script
result = subprocess.run(
    ["bash", 'RockingCurve_generator.sh'],         # シェルスクリプトを呼び出すコマンド
    input=filename,           # 標準入力に渡す値
    text=True,                     # テキストモードを有効化
    capture_output=True            # 出力をキャプチャ
)
print("Standard Error:", result.stderr)
