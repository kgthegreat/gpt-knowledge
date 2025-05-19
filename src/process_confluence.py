
import os
import pypandoc
from tiktoken import get_encoding

# === CONFIGURATION ===
current_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(current_dir, '../data/input/confluence/dp')
OUTPUT_FOLDER = os.path.join(current_dir, '../data/output/confluence/dp')

TEMP_DOCX_FOLDER = os.path.join(current_dir, '../data/output/converted_docx')
OUTPUT_FILE = "merged_confluence_dp.docx"
TOKEN_LIMIT = 2_000_000
FILE_SIZE_LIMIT_MB = 512

encoding = get_encoding("cl100k_base")

def count_tokens(text):
    return len(encoding.encode(text))

def get_file_size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)

def read_doc_file(input_path):
    return pypandoc.convert_file(input_path, 'plain', format='doc')

def write_doc_file(output_path, content):
    pypandoc.convert_text(content, 'doc', format='plain', outputfile=output_path)

def merge_doc_files(input_folder, output_folder, output_file):
    def save_and_reset(content, file_name, token_count):
        with open(file_name, 'w') as f:
            f.write(content)
        print(f"🎉 Saved file: '{file_name}' with ~{token_count} tokens.")
        return "", 0

    merged_content = ""
    total_tokens = 0

    file_index = 1
    current_output_file = os.path.join(output_folder, output_file)
    for filename in sorted(os.listdir(input_folder)):
        if filename.endswith(".doc"):
            path = os.path.join(input_folder, filename)
            text = read_doc_file(path)
            tokens = count_tokens(text)

            if total_tokens + tokens > TOKEN_LIMIT:
                print(f"⚠️ Skipping {filename}: exceeds token limit.")
                merged_content, total_tokens = save_and_reset(merged_content, current_output_file, total_tokens)
                file_index += 1
                current_output_file = os.path.join(output_folder, f"merged_confluence_dp_{file_index}.doc")

            merged_content += text + "\n"
            total_tokens += tokens
            print(f"✅ Added {filename} ({tokens} tokens). Total: {total_tokens}")

            with open(current_output_file, 'w') as f:
                f.write(merged_content)
            if get_file_size_mb(current_output_file) > FILE_SIZE_LIMIT_MB:
                print(f"⛔ File size exceeded after {filename}. Stopping.")
                return

    merged_content, total_tokens = save_and_reset(merged_content, current_output_file, total_tokens)

# === RUN PROCESS ===
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
for filename in os.listdir(INPUT_FOLDER):
    if filename.endswith(".doc") and not filename.startswith("~$"):
        input_path = os.path.join(INPUT_FOLDER, filename)
        output_path = os.path.join(OUTPUT_FOLDER, filename)
        content = read_doc_file(input_path)
        write_doc_file(output_path, content)
        print(f"Processed: {filename}")
