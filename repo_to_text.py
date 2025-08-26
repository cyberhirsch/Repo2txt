import os
import subprocess
import shutil
import stat

# --- Configuration ---
# List of file extensions to include. Add any others you need.
INCLUDED_EXTENSIONS = [
    # Web Development
    ".html", ".css", ".scss", ".js", ".ts", ".tsx", ".jsx", ".json", ".yaml", ".yml",
    ".xml", ".md", "vite.config.ts", "tsconfig.json", "package.json",
    # Python
    ".py", ".pyw", ".ipy",
    # Shell & Config
    ".sh", ".bash", ".csh", ".fish", ".zsh", "Dockerfile", ".env.example", ".conf",
    # C/C++/C#
    ".c", ".cpp", ".h", ".hpp", ".cs",
    # Java & Related
    ".java", ".gradle", ".properties",
    # Other Languages
    ".go", ".rs", ".php", ".rb", ".sql", ".r", ".swift",
    # Data
    ".txt", ".csv"
]

# List of directories and files to exclude.
EXCLUDED_PATTERNS = [
    ".git", ".github", "__pycache__", "node_modules", "vendor", "dist", "build",
    "target", ".venv", "venv", "env", "package-lock.json", "yarn.lock",
    ".DS_Store", "Pods", ".idea", ".vscode",
]

# --- Helper Functions ---

def remove_readonly(func, path, excinfo):
    """
    Error handler for shutil.rmtree.
    If the error is a permission error (common on Windows), it changes the
    file's permissions and retries the deletion.
    """
    # Check if the error is a PermissionError, common on Windows.
    # The `excinfo` tuple contains (type, value, traceback).
    if isinstance(excinfo[1], PermissionError):
        try:
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except Exception as e:
            print(f"Failed to remove readonly attribute from {path}: {e}")
            raise
    else:
        # Re-raise the exception if it's not a permission error we can handle.
        raise

def is_binary(filepath):
    """Check if a file is binary by reading a small chunk."""
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            return b'\x00' in chunk
    except IOError:
        return True

def clone_repo(repo_url, temp_dir):
    """Clones the repository from the given URL into a temporary directory."""
    print(f"Cloning repository: {repo_url}...")
    try:
        subprocess.run(
            ["git", "clone", repo_url, temp_dir],
            check=True,
            capture_output=True,
            text=True
        )
        print("Repository cloned successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e.stderr}")
        raise

def process_repo(source_path, output_file, source_identifier, extensions, exclusions):
    """Walks through the source path and writes file contents to the output file."""
    file_count = 0
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Add the source identifier (URL or local path) as the first line
        outfile.write(f"Source: {source_identifier}\n\n")

        for root, dirs, files in os.walk(source_path):
            # Exclude specified directories from traversal
            dirs[:] = [d for d in dirs if d not in exclusions]

            for file in files:
                # Check for excluded file names/patterns
                if file in exclusions:
                    continue

                # Check for included extensions
                if not any(file.endswith(ext) for ext in extensions):
                    continue
                
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, source_path).replace('\\', '/')

                # Skip binary files
                if is_binary(file_path):
                    print(f"Skipping binary file: {relative_path}")
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                        content = infile.read()
                    
                    outfile.write("=" * 80 + "\n")
                    outfile.write(f"// FILE: {relative_path}\n")
                    outfile.write("=" * 80 + "\n\n")
                    
                    outfile.write(content)
                    outfile.write("\n\n")
                    
                    print(f"Added: {relative_path}")
                    file_count += 1

                except Exception as e:
                    print(f"Error reading file {relative_path}: {e}")
    
    return file_count

def get_repo_name_from_url(url):
    """Extracts the repository name from its URL."""
    return url.split('/')[-1].replace('.git', '')

def main():
    """Main function to prompt user and orchestrate the process."""
    input_path = input("Enter the GitHub repository URL or local directory path: ").strip()
    if not input_path:
        print("No input provided. Exiting.")
        return

    temp_dir = "temp_repo_for_processing"
    
    try:
        # --- Logic for handling GitHub URL ---
        if input_path.startswith(('http://', 'https://')) and 'github.com' in input_path:
            repo_name = get_repo_name_from_url(input_path)
            output_file = f"{repo_name}.txt"
            
            # Clean up old temp directory if it exists
            if os.path.exists(temp_dir):
                print(f"Removing existing temporary directory: {temp_dir}")
                shutil.rmtree(temp_dir, onerror=remove_readonly)
            
            try:
                clone_repo(input_path, temp_dir)
                print("\nProcessing files and concatenating into output file...")
                num_files = process_repo(
                    temp_dir, output_file, input_path, INCLUDED_EXTENSIONS, EXCLUDED_PATTERNS
                )
            finally:
                # Clean up the cloned repository
                if os.path.exists(temp_dir):
                    print(f"\nCleaning up temporary directory: {temp_dir}")
                    shutil.rmtree(temp_dir, onerror=remove_readonly)

        # --- Logic for handling local directory ---
        elif os.path.isdir(input_path):
            print("Local directory detected.")
            # Use the directory's base name for the output file
            repo_name = os.path.basename(os.path.normpath(input_path))
            output_file = f"{repo_name}.txt"
            
            print("\nProcessing files and concatenating into output file...")
            num_files = process_repo(
                input_path, output_file, input_path, INCLUDED_EXTENSIONS, EXCLUDED_PATTERNS
            )

        # --- Handle invalid input ---
        else:
            print("Invalid input. Please provide a valid GitHub URL or an existing local directory path.")
            return

        print("\n" + "="*50)
        print("      SCRIPT COMPLETED SUCCESSFULLY")
        print("="*50)
        print(f"Total files processed: {num_files}")
        print(f"All code has been written to: {output_file}")

    except Exception as e:
        print("\n" + "="*50)
        print("         AN ERROR OCCURRED")
        print("="*50)
        print(f"Details: {e}")

if __name__ == "__main__":
    main()