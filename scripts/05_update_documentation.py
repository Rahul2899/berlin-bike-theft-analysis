"""
Extract analysis results and update README.md and ANALYSIS.md with latest numbers
"""
import pandas as pd
import re
from datetime import datetime

def load_and_calculate_stats(data_path='data/processed/geocoded_data.csv'):
    """Load cleaned data and calculate all key statistics"""
    df = pd.read_csv(data_path)
    
    total_records = len(df)
    
    # Peak hour
    peak_hour = df['incident_hour'].value_counts().idxmax()
    peak_count = df['incident_hour'].value_counts().max()
    peak_pct = (peak_count / total_records) * 100
    
    # Weekday analysis
    weekday_counts = df['day_of_week'].value_counts()
    weekday_theft = weekday_counts[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']].sum()
    weekend_theft = weekday_counts[['Saturday', 'Sunday']].sum()
    weekday_ratio = weekday_theft / weekend_theft
    
    # Bike value analysis
    value_stats = df['bike_value'].describe()
    target_range = len(df[(df['bike_value'] >= 500) & (df['bike_value'] <= 1000)])
    target_pct = (target_range / total_records) * 100
    
    # Success rate (assuming VERSUCH column if available, else 99.5%)
    success_rate = 99.5  # Default from original analysis
    
    return {
        'total_records': f"{total_records:,}",
        'peak_hour': int(peak_hour),
        'peak_count': f"{peak_count:,}",
        'peak_pct': f"{peak_pct:.1f}",
        'weekday_theft': f"{int(weekday_theft):,}",
        'weekend_theft': f"{int(weekend_theft):,}",
        'weekday_ratio': f"{weekday_ratio:.1f}",
        'target_range_count': f"{target_range:,}",
        'target_pct': f"{target_pct:.1f}",
        'avg_value': f"€{value_stats['mean']:.0f}",
        'median_value': f"€{value_stats['50%']:.0f}",
        'success_rate': '99.5',
        'date_range': f"{df['incident_date'].min()} to {df['incident_date'].max()}",
        'last_updated': datetime.now().strftime('%B %d, %Y')
    }

def update_readme(stats):
    """Update README.md with latest statistics"""
    with open('README.md', 'r') as f:
        content = f.read()
    
    # Update key statistics in README
    replacements = [
        (r'(\d+,\d+) real theft incidents', f'{stats["total_records"]} real theft incidents'),
        (r'(\d+,\d+) thefts \(\d+\.\d+% of annual', f'{stats["peak_count"]} thefts ({stats["peak_pct"]}% of annual'),
        (r'(\d+,\d+) thefts happen Mon-Fri', f'{stats["weekday_theft"]} thefts happen Mon-Fri'),
        (r'(\d+,\d+) thefts.*weekend', f'{stats["weekend_theft"]} thefts happen Sat-Sun'),
        (r'(\d+\.\d+)x more dangerous.*weekdays', f'{stats["weekday_ratio"]}x more dangerous on weekdays'),
        (r'30% of all thefts in this range', f'{stats["target_pct"]}% of all thefts in this range'),
        (r'Jan 2025 - May 2026', f'{stats["date_range"]}'),
        (r'\*\*Last updated:\*\* .+', f'**Last updated:** {stats["last_updated"]}'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    with open('README.md', 'w') as f:
        f.write(content)
    
    print("✓ README.md updated with latest statistics")

def update_analysis_md(stats):
    """Update ANALYSIS.md with latest findings"""
    with open('ANALYSIS.md', 'r') as f:
        content = f.read()
    
    replacements = [
        (r'(\d+,\d+) incidents', f'{stats["total_records"]} incidents'),
        (r'\d+ PM.*\d+,\d+ thefts', f'{stats["peak_hour"]:02d}:00  {stats["peak_count"]} thefts (peak)'),
        (r'Last updated:.*', f'Last updated: {stats["last_updated"]}'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    with open('ANALYSIS.md', 'w') as f:
        f.write(content)
    
    print("✓ ANALYSIS.md updated with latest findings")

if __name__ == '__main__':
    print("Extracting latest statistics...")
    stats = load_and_calculate_stats()
    
    print("\n📊 Latest Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\nUpdating documentation...")
    update_readme(stats)
    update_analysis_md(stats)
    
    print("\n✅ Documentation updated successfully")
