import os
import re
import csv
from pathlib import Path

def extract_coordinates_from_file(file_path):
    """Extract x1, y1, x2, y2, x3, y3, x4, y4 coordinates from a bounding box file."""
    coordinates = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    # Find the bounding box data (skip comments)
    in_bbox_section = False
    for line in lines:
        line = line.strip()
        if line.startswith('# Bounding Box'):
            in_bbox_section = True
            continue
        elif line.startswith('#') or not line:
            continue
        elif in_bbox_section:
            # Extract x and y coordinates
            if '\t' in line:
                parts = line.split('\t')
                if len(parts) == 2:
                    try:
                        x = int(parts[0].strip())
                        y = int(parts[1].strip())
                        coordinates.extend([x, y])
                    except ValueError:
                        continue
    
    return coordinates

def extract_id_from_filename(filename):
    """Extract the ID from filename like syn_f000000-0-Pre--front--boundingbox.txt"""
    # Remove the file extension and extract the part before the view type
    basename = filename.replace('--boundingbox.txt', '')
    # Extract everything before --front-- or --left--
    if '--front--' in basename:
        id_part = basename.replace('--front', '')
    elif '--left--' in basename:
        id_part = basename.replace('--left', '')
    else:
        id_part = basename
    
    return id_part

def process_boundingbox_files():
    """Process all bounding box files and create CSV files."""
    
    # Get current directory
    current_dir = Path(__file__).parent
    
    # Find all boundingbox files
    front_files = list(current_dir.glob("*--front--boundingbox.txt"))
    left_files = list(current_dir.glob("*--left--boundingbox.txt"))
    
    print(f"Found {len(front_files)} front files and {len(left_files)} left files")
    
    # Process front files
    front_data = []
    for file_path in front_files:
        coordinates = extract_coordinates_from_file(file_path)
        if len(coordinates) >= 8:  # We need at least 4 points (x1,y1,x2,y2,x3,y3,x4,y4)
            file_id = extract_id_from_filename(file_path.name)
            # According to the request: Id, x1, y1, x2, y2 (taking first two points)
            row = [file_id, coordinates[0], coordinates[1], coordinates[2], coordinates[3]]
            front_data.append(row)
    
    # Process left files
    left_data = []
    for file_path in left_files:
        coordinates = extract_coordinates_from_file(file_path)
        if len(coordinates) >= 8:  # We need at least 4 points (x1,y1,x2,y2,x3,y3,x4,y4)
            file_id = extract_id_from_filename(file_path.name)
            # According to the request: Id, x1, y1, x2, y2 (taking first two points)
            row = [file_id, coordinates[0], coordinates[1], coordinates[2], coordinates[3]]
            left_data.append(row)
    
    # Sort data by ID
    front_data.sort(key=lambda x: x[0])
    left_data.sort(key=lambda x: x[0])
    
    # Write front CSV
    with open('DadosmedidosCSV--front--boundingbox.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Id', 'x1', 'y1', 'x2', 'y2'])  # Header
        writer.writerows(front_data)
    
    # Write left CSV
    with open('DadosmedidosCSV--left--boundingbox.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Id', 'x1', 'y1', 'x2', 'y2'])  # Header
        writer.writerows(left_data)
    
    print(f"Created CSV files:")
    print(f"- DadosmedidosCSV--front--boundingbox.csv with {len(front_data)} records")
    print(f"- DadosmedidosCSV--left--boundingbox.csv with {len(left_data)} records")

if __name__ == "__main__":
    process_boundingbox_files()
