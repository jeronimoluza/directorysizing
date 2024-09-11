import yaml


def load_config(config_path):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def get_unit_multiplier():
    unit_multiplier = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
    return unit_multiplier
