import os
import fnmatch
import time

def search_files_os_walk(root_dir, file_types):
    matches = []
    for root, dirnames, filenames in os.walk(root_dir):
        for file_type in file_types:
            for filename in fnmatch.filter(filenames, file_type):
                matches.append(os.path.join(root, filename))
    return matches

if __name__ == "__main__":
    # Define the root directory to start the search
    root_directory = os.path.expanduser("~\\Downloads")
    # Define the file types to search for
    file_types = [
        "*.py", "*.txt", "*.md",  # Existing file types
        "*.pdf",                  # PDF files
        "*.doc", "*.docx",        # Microsoft Word files
        "*.xls", "*.xlsx",        # Microsoft Excel files
        "*.ppt", "*.pptx"         # Microsoft PowerPoint files
    ]
    # Measure time 
    start_time = time.time()
    found_files_os_walk = search_files_os_walk(root_directory, file_types)
    end_time = time.time()
    os_walk_duration = end_time - start_time
    # Print the found files
    print("Files found using os.walk and fnmatch:")
    for file in found_files_os_walk:
        print(file)
    print(f"\nTime taken using os.walk and fnmatch: {os_walk_duration:.2f} seconds")