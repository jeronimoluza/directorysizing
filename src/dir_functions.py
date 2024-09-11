import os
import utils
import file_functions


def analyze_directories_and_files(directories, size_threshold, units):
    dir_summary = []
    file_summary = []
    unit_multiplier = utils.get_unit_multiplier()

    for directory in directories:
        total_size = 0
        file_count = 0
        large_file_count = 0

        for root, _, files in os.walk(directory):
            for file in files:

                file_data = file_functions.analyze_file(
                    root, file, size_threshold, unit_multiplier
                )

                # Collect file-level data
                file_summary.append(file_data)

        # Append directory-level summary
        dir_summary.append(
            {
                "directory": directory,
                "file_count": file_count,
                "total_size": total_size,
                "large_file_count": large_file_count,
            }
        )

    return dir_summary, file_summary
