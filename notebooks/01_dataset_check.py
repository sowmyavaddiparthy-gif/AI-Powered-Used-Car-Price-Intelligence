from pathlib import Path
import pandas as pd

# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Locate the original dataset
DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "cardekho.csv"

print("=" * 60)
print("USED-CAR DATASET CHECK")
print("=" * 60)

# Check whether the dataset exists
if not DATASET_PATH.exists():
    print("ERROR: Dataset file was not found.")
    print("Expected location:", DATASET_PATH)
else:
    # Load the dataset
    df = pd.read_csv(DATASET_PATH)

    print("\nDataset loaded successfully!")
    print("Number of rows:", df.shape[0])
    print("Number of columns:", df.shape[1])

    print("\nColumn names:")
    for column in df.columns:
        print("-", column)

    print("\nFirst 5 records:")
    print(df.head().to_string(index=False))

    print("\nMissing values in each column:")
    print(df.isnull().sum().to_string())

    print("\nDuplicate rows:", df.duplicated().sum())

    print("\nDataset check completed!")