import yaml


def load_config(config_path):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def get_unit_multiplier():
    unit_multiplier = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
    return unit_multiplier


def human_readable_size(size_bytes):
    """Convert a file size in bytes to a human-readable format (KB, MB, GB, etc.)."""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(min(len(size_name) - 1, (size_bytes).bit_length() // 10))
    power = 1024**i
    size = round(size_bytes / power, 2)
    return f"{size} {size_name[i]}"
