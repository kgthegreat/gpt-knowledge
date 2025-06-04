import json
import os
import os

# Constants for chunking
MAX_FILE_SIZE = 512 * 1024 * 1024  # 512 MB
MAX_TOKENS = 2_000_000
AVG_CHARS_PER_TOKEN = 4  # conservative

def count_tokens(text):
    # Assuming a simple tokenization by splitting on whitespace
    return len(text.split())

def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

def split_file(input_file, output_dir):
    with open(input_file, 'r') as file:
        content = file.read()

    os.makedirs(output_dir, exist_ok=True)
    tokens = content.split()
    num_chunks = (len(tokens) + MAX_TOKENS - 1) // MAX_TOKENS

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    for i in range(num_chunks):
        start = i * MAX_TOKENS
        end = start + MAX_TOKENS
        chunk_content = " ".join(tokens[start:end])
        chunk_file = os.path.join(output_dir, f"{base_name}_chunk_{i+1}.xml")
        with open(chunk_file, 'w') as chunk:
            chunk.write(chunk_content)

def main():
    config_path = 'config/process_xml.json'
    config = load_config(config_path)
    
    input_file = config['input_file']
    output_dir = config['output_directory']
    
    split_file(input_file, output_dir)

if __name__ == "__main__":
    main()
