
import os
import json
import re
from datetime import datetime
from collections import defaultdict

# === CONFIGURATION ===
#INPUT_FOLDER = "/Users/kumargaurav/code/skyscanner/process-slack-archive/data/input/slackdump_20250514_105241/dancing-penguins"
#OUTPUT_FOLDER = "/Users/kumargaurav/code/skyscanner/process-slack-archive/data/output/dp-markdown"
INPUT_FOLDER = "../data/input/slackdump_20250514_105241/rts-queries"
OUTPUT_FOLDER = "../data/output/slack/rts-markdown"

MAX_FILE_SIZE = 512 * 1024 * 1024  # 512 MB
MAX_TOKENS = 2_000_000
AVG_CHARS_PER_TOKEN = 4  # conservative

# === HELPERS ===
def format_timestamp(ts):
    try:
        return datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M")
    except:
        return "Unknown time"

def sanitize_username(profile):
    return profile.get("real_name") or profile.get("display_name") or "Unknown User"

def extract_user_map(messages):
    user_map = {}
    for msg in messages:
        if "user_profile" in msg and "user" in msg:
            user_map[msg["user"]] = sanitize_username(msg["user_profile"])
    return user_map

def replace_user_mentions(text, user_map):
    if not text:
        return ""
    return re.sub(r"<@([A-Z0-9]+)>", lambda m: f"@{user_map.get(m.group(1), m.group(1))}", text)

def format_reactions(msg):
    reactions = msg.get("reactions", [])
    if not reactions:
        return ""
    formatted = []
    for reaction in reactions:
        name = reaction.get("name", "")
        count = reaction.get("count", 0)
        formatted.append(f":{name}: x{count}")
    return f" _(Reactions: {' | '.join(formatted)})_"

def render_thread(messages, user_map):
    threads = defaultdict(list)
    for msg in messages:
        key = msg.get("thread_ts") or msg["ts"]
        threads[key].append(msg)

    thread_blocks = []
    for root_ts, msgs in threads.items():
        msgs.sort(key=lambda m: float(m["ts"]))
        root_msg = msgs[0]
        root_user = user_map.get(root_msg.get("user", ""), "Unknown")
        root_time = format_timestamp(root_msg["ts"])
        raw_text = root_msg.get("text", "").strip()
        root_text = replace_user_mentions(raw_text, user_map)
        root_link = root_msg.get("permalink", "")
        root_reactions = format_reactions(root_msg)

        thread_id = root_ts
        block = [f"### [Thread ID: {thread_id}]\n",
                 f"**Started by:** {root_user}  ",
                 f"**Date:** {root_time}  ",
                 f"**Message:**  \n{root_text}  " + (f"\n{root_reactions}" if root_reactions else "")]

        if root_link:
            block.append(f"[Link to Message]({root_link})")

        if len(msgs) > 1:
            block.append("\n**Replies:**")
            for reply in msgs[1:]:
                user = user_map.get(reply.get("user", ""), "Unknown")
                time = format_timestamp(reply["ts"])
                raw_text = reply.get("text", "").strip()
                text = replace_user_mentions(raw_text, user_map)
                reactions = format_reactions(reply)
                line = f"- **{user} ({time}):** {text}"
                if reactions:
                    line += f" {reactions}"
                block.append(line)

        block.append("\n---\n")
        thread_blocks.append("\n".join(block))

    return thread_blocks

def process_all_files():
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: The directory {INPUT_FOLDER} does not exist.")
        return []
    all_threads = []
    for filename in sorted(os.listdir(INPUT_FOLDER)):
        if filename.endswith(".json"):
            filepath = os.path.join(INPUT_FOLDER, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                messages = json.load(f)
            user_map = extract_user_map(messages)
            threads = render_thread(messages, user_map)
            all_threads.extend(threads)
    return all_threads

def batch_and_save(threads):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    current_batch = []
    current_size = 0
    current_token_est = 0
    file_index = 1

    def write_batch(index, content):
        output_path = os.path.join(OUTPUT_FOLDER, f"slack_batch_{index:02}.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

    for thread in threads:
        encoded = thread.encode("utf-8")
        est_tokens = len(thread) // AVG_CHARS_PER_TOKEN

        if (current_size + len(encoded) > MAX_FILE_SIZE or
            current_token_est + est_tokens > MAX_TOKENS):
            write_batch(file_index, "\n".join(current_batch))
            file_index += 1
            current_batch = []
            current_size = 0
            current_token_est = 0

        current_batch.append(thread)
        current_size += len(encoded)
        current_token_est += est_tokens

    if current_batch:
        write_batch(file_index, "\n".join(current_batch))

    print(f"✅ Created {file_index} markdown file(s) in: {OUTPUT_FOLDER}")

def main():
    threads = process_all_files()
    batch_and_save(threads)

if __name__ == "__main__":
    main()
