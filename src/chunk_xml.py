import json
import os

def load_chunk_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

def split_file(input_file, output_dir, max_size):
    with open(input_file, 'r') as file:
        content = file.read()

    os.makedirs(output_dir, exist_ok=True)
    chunk_size = max_size * 1024 * 1024  # Convert MB to bytes
    num_chunks = (len(content) + chunk_size - 1) // chunk_size

    for i in range(num_chunks):
        start = i * chunk_size
        end = start + chunk_size
        chunk_content = content[start:end]
        chunk_file = os.path.join(output_dir, f"chunk_{i+1}.xml")
        with open(chunk_file, 'w') as chunk:
            chunk.write(chunk_content)

def main():
    config_path = 'config/chunk.json'
    config = load_chunk_config(config_path)
    
    input_file = config['input_file']
    output_dir = config['output_directory']
    max_size = config['max_chunk_size_mb']
    
    split_file(input_file, output_dir, max_size)

if __name__ == "__main__":
    main()
