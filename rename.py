import os
import re

# Define folder path
folder_path = "groundSmoke"

# Get all files in the folder
files = sorted(os.listdir(folder_path))

# Rename files
for file_name in files:
    match = re.match(r"GS(\d+)\.png", file_name)  # Match filenames like GS_0000.png
    if match:
        old_path = os.path.join(folder_path, file_name)
        
        # Convert number (remove leading zeros) and reformat with 3-digit padding
        num = str(int(match.group(1))).zfill(3)  # Ensures '0' -> '000', '191' -> '191'
        
        new_name = f"GS{num}.png"  # Format new filename
        new_path = os.path.join(folder_path, new_name)
        
        os.rename(old_path, new_path)
        print(f"Renamed: {file_name} -> {new_name}")

print("✅ Renaming complete!")
