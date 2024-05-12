import os
import subprocess

def setup_dvc_remote(remote_name, remote_url):
    # Check if the remote is already configured
    result = subprocess.run(f"dvc remote list", shell=True, text=True, capture_output=True)
    if remote_name in result.stdout:
        print(f"DVC remote '{remote_name}' is already configured.")
    else:
        # Add the remote
        subprocess.run(f"dvc remote add -d {remote_name} {remote_url}", shell=True, check=True)
        print(f"DVC remote '{remote_name}' configured with URL: {remote_url}")

def store_data(filename):
    print(f"Starting DVC and Git operations for {filename}")
    
    # Ensure that the file is tracked by DVC
    if not os.path.exists('.dvc'):
        subprocess.run('dvc init --subdir', shell=True, check=True)
        print("DVC initialized.")
    
    # Configure DVC remote if not already configured
    remote_name = 'myremote'
    remote_url = 'gdrive://1JISd6GjxV051UTAjw0nAYjljf'
    setup_dvc_remote(remote_name, remote_url)
    
    # Add the file to DVC tracking
    subprocess.run(f'dvc add {filename}', shell=True, check=True)
    print(f"{filename} added to DVC.")

    # Commit changes to git
    subprocess.run(f'git add {filename}.dvc .gitignore', shell=True, check=True)
    subprocess.run(f'git commit -m "Add/update {filename}"', shell=True, check=True)
    print("Changes committed to Git.")

    # Push the file to the DVC remote
    subprocess.run('dvc push', shell=True, check=True)
    print("Data pushed to DVC remote.")

def main():
    filename = 'data/extracted_data.json'
    print("Current Working Directory:", os.getcwd())
    print("File to be version-controlled:", filename)

    # Ensure file exists before attempting to add to DVC or Git
    if os.path.exists(filename):
        store_data(filename)
    else:
        print(f"Error: The specified file {filename} does not exist.")

if __name__ == "__main__":
    main()
