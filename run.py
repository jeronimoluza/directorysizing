import pandas as pd
from src import dir_functions, file_functions, utils


def main():
    # Load configuration
    config = utils.load_config("config.yaml")
    directories = config["directories"]
    size_threshold = config["file_size_threshold"]
    units = config["units"]

    # Analyze directories
    dir_data = dir_functions.analyze_directories(directories, size_threshold, units)
    dir_df = pd.DataFrame(dir_data)
    dir_df.to_csv("directory_summary.csv", index=False)

    # Analyze files
    file_data = file_functions.analyze_files(directories, units)
    file_df = pd.DataFrame(file_data)
    file_df.to_csv("file_summary.csv", index=False)


if __name__ == "__main__":
    main()
