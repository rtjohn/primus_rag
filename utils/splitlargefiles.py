from openai import OpenAI
import os # needed by OpenAI function?

def split_large_file(file_path, lines_per_file=1500, new_names="big_raw"):
    """
    Splits a large .txt file into smaller files of a specified number of lines.

    Parameters:
    - file_path: Path to the large .txt file.
    - lines_per_file: Number of lines each smaller file should contain.

    Returns:
    - A list of paths to the smaller files created.
    """
    small_files = []
    file_count = 0
    
    try:
        # iterate over the lines in the big file
        with open(file_path, 'r') as large_file:
            while True:
                lines = []
                try:
                    for _ in range(lines_per_file):
                        lines.append(next(large_file)) #iterator over the lines
                except StopIteration:
                    if not lines:
                        break
        # write out the new lines list to a new file
                small_file_path = f"{new_names + file_count}.txt" #should yield "big_raw01.txt" for example        
                try:
                    with open(small_file_path, 'w') as small_file:
                        small_file.writelines(lines)
                        small_files.append(small_file_path)
                except IOError as e:
                    print(f"Error writing to {small_file_path}: {e}")
                    break

                file_count += 1
                if len(lines) < lines_per_file:
                    break
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except PermissionError:
        print(f"Permission denied when trying to read {file_path}.")

    return small_files

# split_large_files usage example:
file_path = '/Users/ryanjohnson/Documents/work/roleplaying_rag/data/big_raw.txt'
small_files = split_large_file(file_path, lines_per_file=100)
print(f"Created {len(small_files)} smaller files:", small_files)


def refine_text_with_gpt(text):
    """
    Uses LLM to refine text by removing unnecessary spaces within words.

    Parameters:
    - text: The text to be refined.

    Returns:
    - The refined text.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        # Without the system message below, the LLM kept trying to complete the text instead of cleaning it.
        messages=[
        {"role": "system", "content": "You are a proofreader.  You cannot generate new content.  Your only capabilities are to review provided content and correct grammatical and typographical errors.  You will not attempt to complete and extend the provided content.  You will only remove unnecessary white spaces within words and your response will include the entirety of the provided text."},
        {"role": "user", "content": "Remove unnecessary spaces within words in the following text:" + text}
        ],
        max_tokens=int(len(text) * 1.1),  # Adjust based on your text length, considering potential expansion
        temperature=0.1,  # A lower temperature for more deterministic outputs
        n=1,
        stop=None
    )
    return response.choices[0].message.content

client = OpenAI()
# Ensure your OpenAI API key is set in your environment variables, or set it here
# openai.api_key = 'your-api-key-here'

def process_files(file_paths):
    """
    Processes a list of file paths, using a LLM to refine the content of each file.

    Parameters:
    - file_paths: A list of paths to the files to be processed.
    """
    # Open each file in the file_paths argument
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                text = file.read()
        except IOError as e:
            print(f"Error reading from {file_path}: {e}")
            continue  # Skip to the next file
        # Send the file to the LLM with the system and user prompt specified in refine_text_with_gpt()
        refined_text = refine_text_with_gpt(text)
        # Clean up the file name
        stripped_file_name = file_path.rsplit(".txt", 1)[0]
        refined_file_path = f"{stripped_file_name}_refined.txt"
        try:
            with open(refined_file_path, 'w') as file:
                file.write(refined_text)
            print(f"Refined file saved to: {refined_file_path}")
        except IOError as e:
            print(f"Error writing to {refined_file_path}: {e}")

# Example usage for process_files
to_be_processed = small_files #small files is the output of split_large_file
process_files(to_be_processed)