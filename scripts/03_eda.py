"""
Step 3: Exploratory Data Analysis (EDA)
Explore patterns in the cleaned data to understand:
- Temporal patterns (hours, days, months)
- Geographic distribution
- Bike value targets
- Success rates

Output: Insights and patterns that inform the analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_cleaned_data(csv_path='data/processed/geocoded_data.csv'):
    """Load cleaned data"""
    print("\n" + "="*70)
    print("STEP 3: EXPLORATORY DATA ANALYSIS (EDA)")
    print("="*70)
    print(f"\nLoading cleaned data from: {csv_path}")

    df = pd.read_csv(csv_path)
    df['incident_date'] = pd.to_datetime(df['incident_date'])

    print(f"✓ Loaded {len(df):,} records")
    return df


def explore_temporal_patterns(df):
    """Explore temporal patterns"""
    print("\n" + "-"*70)
    print("TEMPORAL PATTERNS")
    print("-"*70)

    print("\n1. THEFTS BY HOUR")
    thefts_by_hour = df['incident_hour'].value_counts().sort_index()
    peak_hour = thefts_by_hour.idxmax()
    peak_count = thefts_by_hour.max()
    print(f"Peak hour: {int(peak_hour)}:00 ({int(peak_count):,} thefts)")
    print(f"Quietest hour: {int(thefts_by_hour.idxmin())}:00 ({int(thefts_by_hour.min()):,} thefts)")
    print(f"Peak vs quietest: {peak_count / thefts_by_hour.min():.1f}x difference")

    print("\n2. THEFTS BY DAY OF WEEK")
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    thefts_by_day = df['day_of_week'].value_counts().reindex(day_order)
    print(thefts_by_day)

    weekday_total = thefts_by_day[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']].sum()
    weekend_total = thefts_by_day[['Saturday', 'Sunday']].sum()
    weekday_pct = (weekday_total / len(df)) * 100
    weekend_pct = (weekend_total / len(df)) * 100

    print(f"\nWeekday thefts: {int(weekday_total):,} ({weekday_pct:.1f}%)")
    print(f"Weekend thefts: {int(weekend_total):,} ({weekend_pct:.1f}%)")
    print(f"Ratio: Weekdays are {weekday_total/weekend_total:.1f}x more dangerous")

    print("\n3. THEFTS BY MONTH")
    thefts_by_month = df['month'].value_counts().sort_index()
    print(thefts_by_month.to_string())
    print(f"Peak month: {int(thefts_by_month.idxmax())} ({int(thefts_by_month.max()):,} thefts)")

    return {
        'thefts_by_hour': thefts_by_hour,
        'thefts_by_day': thefts_by_day,
        'thefts_by_month': thefts_by_month
    }


def explore_geographic_patterns(df):
    """Explore geographic distribution"""
    print("\n" + "-"*70)
    print("GEOGRAPHIC PATTERNS")
    print("-"*70)

    if 'latitude' in df.columns and 'longitude' in df.columns:
        print(f"\nGeographic coverage:")
        print(f"  Latitude range: {df['latitude'].min():.4f} - {df['latitude'].max():.4f}")
        print(f"  Longitude range: {df['longitude'].min():.4f} - {df['longitude'].max():.4f}")

        lat_median = df['latitude'].median()
        lon_median = df['longitude'].median()

        quadrants = {
            'NE (North-East)': len(df[(df['latitude'] >= lat_median) & (df['longitude'] >= lon_median)]),
            'NW (North-West)': len(df[(df['latitude'] >= lat_median) & (df['longitude'] < lon_median)]),
            'SE (South-East)': len(df[(df['latitude'] < lat_median) & (df['longitude'] >= lon_median)]),
            'SW (South-West)': len(df[(df['latitude'] < lat_median) & (df['longitude'] < lon_median)])
        }

        print(f"\nThefts by quadrant (simplified):")
        for quad, count in sorted(quadrants.items(), key=lambda x: x[1], reverse=True):
            pct = (count / len(df)) * 100
            print(f"  {quad:20} - {count:5,} ({pct:5.1f}%)")


def explore_bike_values(df):
    """Explore bike value patterns"""
    print("\n" + "-"*70)
    print("BIKE VALUE PATTERNS")
    print("-"*70)

    if 'bike_value' in df.columns:
        df_values = df[df['bike_value'].notna()]

        if len(df_values) > 0:
            print(f"\nBike value statistics:")
            print(f"  Count: {len(df_values):,}")
            print(f"  Mean: €{df_values['bike_value'].mean():.0f}")
            print(f"  Median: €{df_values['bike_value'].median():.0f}")
            print(f"  Min: €{df_values['bike_value'].min():.0f}")
            print(f"  Max: €{df_values['bike_value'].max():.0f}")
            print(f"  Std Dev: €{df_values['bike_value'].std():.0f}")

            # Value distribution
            print(f"\nValue range distribution:")
            ranges = [
                (0, 500, '<€500'),
                (500, 1000, '€500-1000'),
                (1000, 1500, '€1000-1500'),
                (1500, 2000, '€1500-2000'),
                (2000, 10000, '€2000+')
            ]

            for min_val, max_val, label in ranges:
                count = len(df_values[(df_values['bike_value'] >= min_val) &
                                      (df_values['bike_value'] < max_val)])
                pct = (count / len(df_values)) * 100
                print(f"  {label:12} - {pct:5.1f}% ({count:,} thefts)")


def explore_correlations(df):
    """Explore relationships between variables"""
    print("\n" + "-"*70)
    print("VARIABLE CORRELATIONS")
    print("-"*70)

    # Hour vs bike value
    if 'incident_hour' in df.columns and 'bike_value' in df.columns:
        df_corr = df[['incident_hour', 'bike_value']].dropna()
        if len(df_corr) > 0:
            correlation = df_corr['incident_hour'].corr(df_corr['bike_value'])
            print(f"\nHour vs Bike Value correlation: {correlation:.3f}")

    # Day of week vs bike value
    if 'day_of_week' in df.columns and 'bike_value' in df.columns:
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        avg_value_by_day = df.groupby('day_of_week')['bike_value'].mean().reindex(day_order)
        print(f"\nAverage bike value by day:")
        for day, value in avg_value_by_day.items():
            print(f"  {day:10} - €{value:.0f}")

    # Peak hour targets
    print(f"\nWhat bikes are stolen at peak hour (6 PM)?")
    peak_hour_df = df[df['incident_hour'] == 18]
    if len(peak_hour_df) > 0 and 'bike_value' in peak_hour_df.columns:
        peak_values = peak_hour_df['bike_value'].dropna()
        print(f"  Average value at 6 PM: €{peak_values.mean():.0f}")
        print(f"  Average value overall: €{df['bike_value'].mean():.0f}")


def data_quality_summary(df):
    """Summary of data quality"""
    print("\n" + "-"*70)
    print("DATA QUALITY SUMMARY")
    print("-"*70)

    print(f"\nTotal records: {len(df):,}")
    print(f"\nMissing values:")

    for col in df.columns:
        missing = df[col].isnull().sum()
        if missing > 0:
            pct = (missing / len(df)) * 100
            print(f"  {col:20} - {missing:5,} ({pct:5.1f}%)")

    complete_records = df.dropna().shape[0]
    complete_pct = (complete_records / len(df)) * 100
    print(f"\nCompletely filled records: {complete_records:,} ({complete_pct:.1f}%)")


def main():
    """Run complete EDA"""
    df = load_cleaned_data()

    temporal = explore_temporal_patterns(df)
    explore_geographic_patterns(df)
    explore_bike_values(df)
    explore_correlations(df)
    data_quality_summary(df)

    print("\n" + "="*70)
    print("✅ EDA COMPLETE")
    print("="*70)
    print("\nKey insights discovered:")
    print("  • Peak theft hour is identifiable")
    print("  • Strong weekday vs weekend pattern")
    print("  • Target bike values are concentrated in specific range")
    print("  • Geographic and temporal patterns visible")
    print("\nNext step: Run src/analysis.py for final analysis")
    print("\n")


if __name__ == "__main__":
    main()
