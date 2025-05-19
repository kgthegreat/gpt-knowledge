import os
from PyPDF2 import PdfReader, PdfWriter

# === CONFIGURATION ===
current_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(current_dir, '../data/input/confluence/dp')
OUTPUT_FOLDER = os.path.join(current_dir, '../data/output/confluence/dp')
OUTPUT_FILE = "merged_confluence_dp.pdf"
TOKEN_LIMIT = 2_000_000
FILE_SIZE_LIMIT_MB = 256

def get_file_size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)

def count_tokens(text):
    # Assuming an average of 4 characters per token
    return len(text) // 4

def merge_pdfs(input_folder, output_folder, output_file):
    os.makedirs(output_folder, exist_ok=True)
    writer = PdfWriter()
    total_tokens = 0
    current_output_file = os.path.join(output_folder, output_file)

    for filename in sorted(os.listdir(input_folder)):
        if filename.endswith(".pdf"):
            path = os.path.join(input_folder, filename)
            reader = PdfReader(path)
            for page in reader.pages:
                text = page.extract_text() or ""
                tokens = count_tokens(text)
                if total_tokens + tokens > TOKEN_LIMIT:
                    print(f"⚠️ Skipping {filename}: exceeds token limit.")
                    break
                writer.add_page(page)
                total_tokens += tokens
                if get_file_size_mb(current_output_file) > FILE_SIZE_LIMIT_MB:
                    print(f"⛔ File size exceeded after {filename}. Stopping.")
                    return

    with open(current_output_file, 'wb') as f:
        writer.write(f)
    print(f"🎉 Merged PDF saved as '{current_output_file}' with ~{total_tokens} tokens.")

if __name__ == "__main__":
    merge_pdfs(INPUT_FOLDER, OUTPUT_FOLDER, OUTPUT_FILE)
