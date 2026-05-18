"""
Step 1: Load and Inspect Raw Data
Load the original Berlin bike theft data from the official open data portal
and perform initial exploration.

Output: Summary of raw data structure, size, and quality
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_raw_data(csv_path='data/raw/Fahrraddiebstahl.csv'):
    """Load the raw Berlin bike theft data"""
    print("\n" + "="*70)
    print("STEP 1: LOADING RAW DATA")
    print("="*70)

    print(f"\nLoading from: {csv_path}")
    df = pd.read_csv(csv_path, encoding='latin-1')

    print(f"✓ Loaded successfully")
    print(f"\nDataset shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

    return df


def inspect_data(df):
    """Inspect raw data structure and quality"""
    print("\n" + "-"*70)
    print("DATA STRUCTURE")
    print("-"*70)

    print("\nColumn names and types:")
    print(df.dtypes)

    print("\n" + "-"*70)
    print("FIRST FEW ROWS")
    print("-"*70)
    print(df.head())

    print("\n" + "-"*70)
    print("DATA QUALITY SUMMARY")
    print("-"*70)

    print("\nMissing values:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    quality = pd.DataFrame({
        'Column': df.columns,
        'Missing': missing.values,
        'Missing %': missing_pct.values
    })
    print(quality.to_string(index=False))

    print("\n" + "-"*70)
    print("BASIC STATISTICS")
    print("-"*70)
    print(df.describe())

    print("\n" + "-"*70)
    print("MEMORY USAGE")
    print("-"*70)
    print(f"Total memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    return quality


def check_date_range(df):
    """Check temporal coverage"""
    print("\n" + "-"*70)
    print("TEMPORAL COVERAGE")
    print("-"*70)

    # Find date columns
    date_cols = df.select_dtypes(include=['object']).columns

    for col in date_cols:
        try:
            dates = pd.to_datetime(df[col], errors='coerce')
            valid_dates = dates.notna().sum()
            if valid_dates > 0:
                print(f"\n{col}:")
                print(f"  Valid dates: {valid_dates:,}")
                print(f"  Date range: {dates.min()} to {dates.max()}")
                print(f"  Duration: {(dates.max() - dates.min()).days} days")
        except:
            pass


def main():
    """Run data loading and inspection"""
    df = load_raw_data()
    quality = inspect_data(df)
    check_date_range(df)

    print("\n" + "="*70)
    print("✅ RAW DATA LOADED AND INSPECTED")
    print("="*70)
    print("\nNext step: Run 02_data_cleaning.py to clean and transform")
    print("\n")

    return df


if __name__ == "__main__":
    df = main()
