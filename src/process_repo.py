import json
import os
import subprocess

def load_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

def run_repomix(repo_url, output_file, ignore_files):
    # Construct the repomix command
    command = ["repomix", "--remote", repo_url, "-o", output_file]
    ignore_pattern = ",".join(ignore_files)
    command.extend(["-i", ignore_pattern])
    
    # Print the command for auditing
    print("Running command:", " ".join(command))
    
    subprocess.run(command, check=True)

def main():
    config_path = 'config/repomix_config.json'
    config = load_config(config_path)
    
    output_directory = config['output_directory']
    os.makedirs(output_directory, exist_ok=True)
    
    for repo_url in config['repositories']:
        repo_name = os.path.basename(repo_url).replace('.git', '')
        output_file = os.path.join(output_directory, f"{repo_name}.xml")
        run_repomix(repo_url, output_file, config['ignore_files'])

if __name__ == "__main__":
    main()
