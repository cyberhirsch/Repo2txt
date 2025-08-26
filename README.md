# Repo2txt

A Python script that clones a GitHub/GitLab repository or uses a local directory and concatenates all relevant source code into one or more `.txt` files. It's designed to easily provide codebase context to Large Language Models (LLMs), for code analysis, or for archiving.

## Key Features

-   **Supports Remote & Local:** Works with public GitHub/GitLab URLs and local directories.
-   **Intelligent File Filtering:** Includes common source code extensions and excludes unnecessary directories (`node_modules`, `.git`, `builds`, etc.) by default.
-   **Customizable:** Easily edit the Python lists `INCLUDED_EXTENSIONS` and `EXCLUDED_PATTERNS` to fit your project's needs.
-   **Output Splitting:** Optionally split the output into multiple files based on a specified word count, perfect for fitting within LLM context limits.
-   **Automatic Cleanup:** Deletes the cloned repository automatically after processing.

## Prerequisites

-   [Python 3.6+](https://www.python.org/downloads/)
-   [Git](https://git-scm.com/downloads)

## How to Use

1.  **Download:** On windows run run.bat
2.  **Follow the prompts:**
    -   Enter the repository URL (GitHub or GitLab) or the path to your local directory.
    -   Choose if you want to split the output into multiple files.
    -   If splitting, enter the maximum word count per file.
3.  **Done!** The output `.txt` file(s) will be created in the same directory.

## License

This project is licensed under the MIT License.
