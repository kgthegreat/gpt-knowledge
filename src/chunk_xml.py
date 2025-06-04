import json
import os

def load_chunk_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

def count_tokens(text):
    # Assuming a simple tokenization by splitting on whitespace
    return len(text.split())

def split_file(input_file, output_dir, max_tokens):
    with open(input_file, 'r') as file:
        content = file.read()

    os.makedirs(output_dir, exist_ok=True)
    tokens = content.split()
    num_chunks = (len(tokens) + max_tokens - 1) // max_tokens

    for i in range(num_chunks):
        start = i * max_tokens
        end = start + max_tokens
        chunk_content = " ".join(tokens[start:end])
        chunk_file = os.path.join(output_dir, f"chunk_{i+1}.xml")
        with open(chunk_file, 'w') as chunk:
            chunk.write(chunk_content)

def main():
    config_path = 'config/chunk.json'
    config = load_chunk_config(config_path)
    
    input_file = config['input_file']
    output_dir = config['output_directory']
    max_tokens = config['max_chunk_size_tokens']
    
    split_file(input_file, output_dir, max_size)

if __name__ == "__main__":
    main()
