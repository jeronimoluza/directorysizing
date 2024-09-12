# Directory and File Size Analyzer

This project analyzes the sizes and counts of files within directories and S3 buckets specified in `config.yaml` and outputs two CSV files:

- `directory_summary.csv`: Summarizes file counts and total sizes per folder.
- `file_summary.csv`: Lists file sizes and their parent folder.

## How to Run

1. Specify directories and size thresholds in `configs/config.yaml`.
2. Run the project with:

```bash
make run
```

## Project Structure

- `run.py`: Entry point to execute the analysis.
- `configs/config.yaml`: Configuration file specifying directories and thresholds.
- `Makefile`: Allows running the project with `make`.
- `src/functions.py`: File and directory extraction functions.
- `src/utils.py`: Utility functions, such as reading `config.yaml`.
