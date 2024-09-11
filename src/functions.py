import os
import boto3
from src import utils
from tqdm import tqdm


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

        print("Walking directory structure: %s" % directory)
        tuples = list(os.walk(directory))
        for root, _, files in tqdm(tuples):
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
                        "dir_id": dir_id,
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

        print("Finished processing directory: %s" % directory)

    return dir_summary, file_summary


def analyze_s3_buckets(buckets, size_threshold, units):
    s3_client = boto3.client("s3")
    dir_summary = []
    file_summary = []

    # Unit multiplier for converting to bytes
    unit_multiplier = utils.get_unit_multiplier()

    # Convert size_threshold to bytes using the unit_multiplier
    size_threshold_in_bytes = size_threshold * unit_multiplier[units]

    dir_id = 1  # Unique ID counter for directory summary
    file_id = 1  # Unique ID counter for file summary

    for s3_path in buckets:
        bucket_name, prefix = s3_path.replace("s3://", "").split("/", 1)
        total_size_bytes = 0
        file_count = 0
        large_file_count = 0

        print("Walking S3 bucket: %s" % s3_path)
        paginator = s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)

        for page in pages:
            if "Contents" not in page:
                continue

            for obj in page["Contents"]:
                file_size_bytes = obj["Size"]
                file_key = obj["Key"]

                # Accumulate bucket-level data
                total_size_bytes += file_size_bytes
                file_count += 1

                # Check if the file size is larger than the threshold
                if file_size_bytes > size_threshold_in_bytes:
                    large_file_count += 1

                # Collect file-level data
                file_summary.append(
                    {
                        "file_id": file_id,  # Add unique ID for each file
                        "file_name": file_key.split("/")[-1],
                        "file_size_bytes": file_size_bytes,
                        "file_size_h": utils.human_readable_size(file_size_bytes),
                        "parent_directory": "/".join(file_key.split("/")[:-1]),
                        "file_path": f"s3://{bucket_name}/{file_key}",
                        "source_folder": f"s3://{bucket_name}/{prefix}",
                        "dir_id": dir_id,
                    }
                )
                file_id += 1  # Increment file ID

        # Append bucket-level summary
        dir_summary.append(
            {
                "directory_id": dir_id,  # Add unique ID for each bucket
                "directory": f"s3://{bucket_name}/{prefix}",
                "file_count": file_count,
                "total_size_bytes": total_size_bytes,
                "total_size_h": utils.human_readable_size(total_size_bytes),
                "large_file_count": large_file_count,
            }
        )
        dir_id += 1  # Increment directory ID

    return dir_summary, file_summary


def analyze_paths(paths, size_threshold, units):
    s3_paths = [path for path in paths if path.startswith("s3://")]
    local_paths = [
        path
        for path in paths
        if (not path.startswith("s3://")) and (os.path.isdir(path))
    ]

    dirs_buckets_summaries = []
    file_summaries = []

    if s3_paths:
        s3_buckets_summary, s3_file_summary = analyze_s3_buckets(
            s3_paths, size_threshold, units
        )
        dirs_buckets_summaries.extend(s3_buckets_summary)
        file_summaries.extend(s3_file_summary)

    if local_paths:
        dir_summary, file_summary = analyze_directories(
            local_paths, size_threshold, units
        )
        dirs_buckets_summaries.extend(dir_summary)
        file_summaries.extend(file_summary)

    return dirs_buckets_summaries, file_summaries
