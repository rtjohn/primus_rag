import os
import math

def list_txt_files(directory):
    """List all .txt files in the given directory."""
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.txt')]

def combine_files(file_paths, target_directory, files_per_combined_file):
    """Combine multiple .txt files into fewer larger ones."""
    # Check if target directory exists, create if not
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        print(f"Created directory: {target_directory}")

    combined_file_contents = []
    combined_file_count = 0

    for index, file_path in enumerate(file_paths):
        with open(file_path, 'r') as file:
            combined_file_contents.append(file.read())

        # Combine files or if it's the last file in the list
        if (index + 1) % files_per_combined_file == 0 or (index + 1) == len(file_paths):
            combined_file_name = os.path.join(target_directory, f"combined_file_{combined_file_count}.txt")
            with open(combined_file_name, 'w') as combined_file:
                combined_file.write("\n".join(combined_file_contents))
            print(f"Created {combined_file_name}")
            combined_file_contents = []  # Reset for the next batch
            combined_file_count += 1


# Configuration
source_directory = '/Users/ryanjohnson/Documents/work/roleplaying_rag/data/phb5e_refined'
os.chdir(source_directory)  
target_directory = '/Users/ryanjohnson/Documents/work/roleplaying_rag/data/phb5e_refined/combined'  # Target directory for the combined .txt files
total_files = 845  # Total number of .txt files you have
target_combined_files = 100  # Desired number of combined .txt files

# Calculate how many original .txt files should go into each combined file
files_per_combined_file = math.ceil(total_files / target_combined_files)

# List all .txt files in the source directory
txt_files = list_txt_files(source_directory)
txt_files

# Combine the .txt files
combine_files(txt_files, target_directory, files_per_combined_file)

