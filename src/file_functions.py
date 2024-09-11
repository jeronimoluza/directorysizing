import os
import utils


def analyze_file(root, file, units, size_threshold, unit_multiplier):
    file_path = os.path.join(root, file)
    file_size = os.path.getsize(file) / unit_multiplier[units]

    # Accumulate directory-level data
    total_size += file_size
    file_count += 1
    if file_size > size_threshold:
        large_file_count += 1

    result = {
        "file_name": file,
        "file_size": file_size,
        "parent_directory": root,
        "file_path": file_path,
    }

    return result
