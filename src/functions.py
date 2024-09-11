import os
from src import utils


def analyze_directories(directories, size_threshold, units):
    dir_summary = []
    file_summary = []

    # Unit multiplier for converting to bytes
    unit_multiplier = utils.get_unit_multiplier()

    # Convert size_threshold to bytes using the unit_multiplier
    size_threshold_in_bytes = size_threshold * unit_multiplier[units]

    dir_id = 1  # Unique ID counter for directory summary
    file_id = 1  # Unique ID counter for file summary

    for directory in directories:
        assert os.path.isdir(directory), "Directory %s does not exist" % directory
        total_size_bytes = 0
        file_count = 0
        large_file_count = 0

        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if not os.path.isfile(file_path):
                    continue
                file_size_bytes = os.path.getsize(file_path)

                # Accumulate directory-level data
                total_size_bytes += file_size_bytes
                file_count += 1

                # Check if the file size is larger than the threshold
                if file_size_bytes > size_threshold_in_bytes:
                    large_file_count += 1

                # Collect file-level data
                file_summary.append(
                    {
                        "id": file_id,
                        "file_name": file,
                        "file_size_bytes": file_size_bytes,
                        "file_size_h": utils.human_readable_size(file_size_bytes),
                        "parent_directory": root,
                        "file_path": file_path,
                        "source_folder": directory,
                    }
                )
                file_id += 1

        # Append directory-level summary
        dir_summary.append(
            {
                "id": dir_id,
                "directory": directory,
                "file_count": file_count,
                "total_size_bytes": total_size_bytes,
                "total_size_h": utils.human_readable_size(total_size_bytes),
                "large_file_count": large_file_count,
            }
        )
        dir_id += 1

    return dir_summary, file_summary
