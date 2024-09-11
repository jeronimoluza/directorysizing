import pandas as pd
from src import functions, utils


def main():
    # Load configuration
    config = utils.load_config("dev_config.yaml")
    directories = config["directories"]
    size_threshold = config["file_size_threshold"]
    units = config["units"]

    # Analyze directories
    dir_data, file_data = functions.analyze_directories(
        directories, size_threshold, units
    )
    dir_df = pd.DataFrame(dir_data)
    dir_df.to_csv("directory_summary.csv", index=False)

    file_df = pd.DataFrame(file_data)
    file_df.to_csv("file_summary.csv", index=False)


if __name__ == "__main__":
    main()
