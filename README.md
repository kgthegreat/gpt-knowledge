# GPT Knowledge Tools

Helps build knowledge for custom GPTs.

## Usage

The `src` directory contains scripts used to prepare PDF and Slack data for ingestion by custom GPTs.

### process_pdfs.py

Merges PDF files from `data/input/confluence/dp` into a single file located at `data/output/confluence/dp/merged_confluence_dp.pdf`. Edit the constants at the top of the script to adjust the input and output locations.

Run the script with:

```bash
python src/process_pdfs.py
```

### process_slack.py

Converts Slack export JSON files found in `data/input/slackdump_20250514_105241/rts-queries` into Markdown batches saved under `data/output/slack/rts-markdown`.
Modify the configuration constants if your directories differ.

Run the script with:

```bash
python src/process_slack.py
```

Both scripts assume Python 3.10+ and require `PyPDF2` for PDF processing.

### repomix_output.py

This script reads from a configuration file and runs the `repomix` command for each repository listed. The output for each repository is saved in the specified output directory.

#### Usage

1. Configure the `config/repomix_config.json` file with your repositories, output directory, and files to ignore.
2. Run the script:

   ```bash
   python src/repomix_output.py
   ```

3. The output files will be named after each repository and saved in the specified output directory.

