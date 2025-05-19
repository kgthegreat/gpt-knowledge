
import os
import subprocess
from docx import Document
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

def convert_doc_to_docx(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        if filename.endswith(".doc") and not filename.startswith("~$"):
            input_path = os.path.join(input_folder, filename)
            subprocess.run([
                "soffice", "--headless", "--convert-to", "docx", "--outdir", output_folder, input_path
            ], check=True)
            print(f"Converted: {filename}")

def merge_docx_files(input_folder, output_folder, output_file):
    def save_and_reset(doc, file_name, token_count):
        doc.save(file_name)
        print(f"🎉 Saved file: '{file_name}' with ~{token_count} tokens.")
        return Document(), 0
    merged_doc = Document()
    total_tokens = 0

    file_index = 1
    current_output_file = os.path.join(output_folder, output_file)
    for filename in sorted(os.listdir(input_folder)):
        if filename.endswith(".docx"):
            path = os.path.join(input_folder, filename)
            doc = Document(path)
            text = "\n".join([p.text for p in doc.paragraphs])
            tokens = count_tokens(text)

            if total_tokens + tokens > TOKEN_LIMIT:
                print(f"⚠️ Skipping {filename}: exceeds token limit.")
                merged_doc, total_tokens = save_and_reset(merged_doc, current_output_file, total_tokens)
                file_index += 1
                current_output_file = os.path.join(output_folder, f"merged_confluence_dp_{file_index}.docx")

            for para in doc.paragraphs:
                merged_doc.add_paragraph(para.text)

            total_tokens += tokens
            print(f"✅ Added {filename} ({tokens} tokens). Total: {total_tokens}")

            merged_doc.save(current_output_file)
            if get_file_size_mb(current_output_file) > FILE_SIZE_LIMIT_MB:
                print(f"⛔ File size exceeded after {filename}. Stopping.")
                return

    merged_doc, total_tokens = save_and_reset(merged_doc, current_output_file, total_tokens)

# === RUN PROCESS ===
convert_doc_to_docx(INPUT_FOLDER, TEMP_DOCX_FOLDER)
merge_docx_files(TEMP_DOCX_FOLDER, OUTPUT_FOLDER, OUTPUT_FILE)
