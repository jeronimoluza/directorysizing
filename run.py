import pandas as pd
from src import functions, utils


def run(config_path="configs/config.yaml"):
    # Load configuration
    config = utils.load_config(config_path=config_path)
    directories = config["directories"]
    size_threshold = config["file_size_threshold"]
    units = config["units"]

    # Analyze directories
    dir_data, file_data = functions.analyze_paths(directories, size_threshold, units)
    dir_df = pd.DataFrame(dir_data)
    dir_df.to_csv("directory_summary.csv", index=False)

    file_df = pd.DataFrame(file_data)
    file_df.to_csv("file_summary.csv", index=False)


def devrun():
    run(config_path="configs/dev_config.yaml")
