import os
import fnmatch
import time
import csv
from functools import wraps
from docx import Document
from openpyxl import load_workbook
from pptx import Presentation
import pythoncom
from win32com.client import Dispatch
import xlrd

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"\nTime taken by {func.__name__}: {duration:.2f} seconds")
        return result
    return wrapper

def search_files_os_walk(root_dir, file_types):
    matches = []
    for root, dirnames, filenames in os.walk(root_dir):
        for file_type in file_types:
            for filename in fnmatch.filter(filenames, file_type):
                matches.append(os.path.join(root, filename))
    return matches

def read_doc_file(file_path):
    pythoncom.CoInitialize()
    word = Dispatch("Word.Application")
    doc = word.Documents.Open(file_path)
    file_data = ' '.join([para.Range.Text for para in doc.Paragraphs])
    doc.Close()
    word.Quit()
    return file_data

def get_file_info(file_path):
    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_path)[1]
    file_size = os.path.getsize(file_path)
    file_data = ""
    
    try:
        if file_type.lower() == ".doc":
            file_data = read_doc_file(file_path)
        elif file_type.lower() == ".docx":
            doc = Document(file_path)
            file_data = ' '.join([para.text for para in doc.paragraphs])
        elif file_type.lower() == ".xls":
            wb = xlrd.open_workbook(file_path)
            file_data = ' '.join([str(cell.value) for sheet in wb.sheets() for row in range(sheet.nrows) for cell in sheet.row(row)])
        elif file_type.lower() == ".xlsx":
            wb = load_workbook(file_path, read_only=True, data_only=True)
            file_data = ' '.join([str(cell.value) for sheet in wb for row in sheet.iter_rows() for cell in row])
        elif file_type.lower() in [".ppt", ".pptx"]:
            prs = Presentation(file_path)
            file_data = ' '.join([shape.text for slide in prs.slides for shape in slide.shapes if hasattr(shape, "text")])
        elif file_type.lower() != ".pdf":
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                file_data = file.read().replace('\n', ' ').replace('\r', ' ')
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return file_name, file_type, file_size, file_data

@timer
def write_file_info_to_csv(file_paths, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['File Name', 'File Type', 'File Size', 'File Data'])
        for file_path in file_paths:
            try:
                file_info = get_file_info(file_path)
                csv_writer.writerow(file_info)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    print(f"\nFile information has been written to {csv_file_path}")

@timer
def main():
    # Define the root directory to start the search
    root_directory = os.path.expanduser("~\\Downloads")
    
    # Define the file types to search for
    file_types = [
        "*.txt", "*.md",  # Existing file types
        "*.pdf",          # PDF files
        "*.doc", "*.docx",# Microsoft Word files
        "*.xls", "*.xlsx",# Microsoft Excel files
        "*.ppt", "*.pptx" # Microsoft PowerPoint files
    ]
    
    # Search for files using os.walk and fnmatch
    found_files_os_walk = search_files_os_walk(root_directory, file_types)
    
    # Print the found files using os.walk and fnmatch
    print("Files found using os.walk and fnmatch:")
    for file in found_files_os_walk:
        print(file)
    
    # Write file information to CSV
    csv_file_path = os.path.join(os.getcwd(), 'file_info.csv')
    write_file_info_to_csv(found_files_os_walk, csv_file_path)

if __name__ == "__main__":
    main()