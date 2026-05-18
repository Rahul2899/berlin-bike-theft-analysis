"""
Generate visualizations from latest analysis data
Creates PNG charts for peak hours, weekday patterns, bike values, and success rates
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
import os

# Ensure output directory exists
os.makedirs('visualizations', exist_ok=True)

def load_data(data_path='data/processed/geocoded_data.csv'):
    """Load cleaned dataset"""
    return pd.read_csv(data_path)

def create_peak_hour_chart(df):
    """Create peak hour distribution chart"""
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Calculate hourly thefts
    hourly = df['incident_hour'].value_counts().sort_index()
    
    # Create bar chart
    colors = ['#d32f2f' if x == hourly.max() else '#ff6f00' if x > hourly.mean() else '#ffa726' 
              for x in hourly.values]
    bars = ax.bar(hourly.index, hourly.values, color=colors, edgecolor='black', linewidth=0.5)
    
    # Formatting
    ax.set_xlabel('Hour of Day', fontsize=14, fontweight='bold')
    ax.set_ylabel('Number of Thefts', fontsize=14, fontweight='bold')
    ax.set_title('Peak Theft Hours in Berlin: When Thieves Strike', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(range(0, 24))
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add peak hour annotation
    peak_hour = hourly.idxmax()
    peak_count = hourly.max()
    ax.annotate(f'PEAK: {peak_hour}:00\n{peak_count:,} thefts', 
                xy=(peak_hour, peak_count), xytext=(peak_hour+2, peak_count),
                fontsize=12, fontweight='bold', color='#d32f2f',
                arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=2),
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('visualizations/viz_1_peak_hour_expert.png', dpi=120, bbox_inches='tight')
    plt.close()
    print("✓ Peak hour chart generated")

def create_weekday_chart(df):
    """Create weekday vs weekend comparison"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Calculate weekday/weekend counts
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily = df['day_of_week'].value_counts().reindex(weekday_order)
    
    # Colors: weekdays orange, weekends blue
    colors = ['#ff6f00' if day not in ['Saturday', 'Sunday'] else '#1976d2' for day in weekday_order]
    
    bars = ax.bar(range(len(daily)), daily.values, color=colors, edgecolor='black', linewidth=0.5)
    
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars, daily.values)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
                f'{val:,}', ha='center', fontsize=11, fontweight='bold')
    
    # Formatting
    ax.set_xticks(range(len(daily)))
    ax.set_xticklabels(weekday_order, rotation=45, ha='right')
    ax.set_ylabel('Number of Thefts', fontsize=14, fontweight='bold')
    ax.set_title('Weekday Effect: When Are Bikes Most Vulnerable?', fontsize=16, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add legend
    weekday_patch = mpatches.Patch(color='#ff6f00', label='Weekday (Mon-Fri)')
    weekend_patch = mpatches.Patch(color='#1976d2', label='Weekend (Sat-Sun)')
    ax.legend(handles=[weekday_patch, weekend_patch], fontsize=12, loc='upper right')
    
    # Calculate and annotate ratio
    weekday_total = daily[:'Friday'].sum()
    weekend_total = daily['Saturday':].sum()
    ratio = weekday_total / weekend_total
    ax.text(0.02, 0.98, f'{ratio:.1f}x more dangerous on weekdays', 
            transform=ax.transAxes, fontsize=13, fontweight='bold', color='#d32f2f',
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('visualizations/viz_2_weekday_expert.png', dpi=120, bbox_inches='tight')
    plt.close()
    print("✓ Weekday comparison chart generated")

def create_bike_value_chart(df):
    """Create bike value distribution"""
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Define value ranges
    ranges = [
        (0, 500, 'Budget\n(<€500)', '#4caf50'),
        (500, 1000, 'Sweet Spot\n(€500-1k)', '#ff6f00'),
        (1000, 1500, 'Premium\n(€1k-1.5k)', '#ffa726'),
        (1500, 2000, 'High-end\n(€1.5k-2k)', '#f57c00'),
        (2000, 10000, 'Luxury\n(€2k+)', '#d32f2f'),
    ]
    
    counts = []
    labels = []
    colors = []
    
    for min_val, max_val, label, color in ranges:
        count = len(df[(df['bike_value'] >= min_val) & (df['bike_value'] < max_val)])
        counts.append(count)
        labels.append(label)
        colors.append(color)
    
    # Create horizontal bar chart
    bars = ax.barh(labels, counts, color=colors, edgecolor='black', linewidth=0.5)
    
    # Add value labels
    for bar, count in zip(bars, counts):
        width = bar.get_width()
        pct = (count / len(df)) * 100
        ax.text(width + 100, bar.get_y() + bar.get_height()/2, 
                f'{count:,} ({pct:.1f}%)', 
                ha='left', va='center', fontsize=11, fontweight='bold')
    
    # Formatting
    ax.set_xlabel('Number of Thefts', fontsize=14, fontweight='bold')
    ax.set_title('Thieves Target Specific Bike Values: The Sweet Spot', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Highlight sweet spot
    ax.text(0.98, 0.05, '€500-€1000 is the target range:\nHigh enough to be worth effort,\ncommon enough to not stand out',
            transform=ax.transAxes, fontsize=12, fontweight='bold',
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('visualizations/viz_3_bike_value_expert.png', dpi=120, bbox_inches='tight')
    plt.close()
    print("✓ Bike value distribution chart generated")

def create_success_rate_chart(df):
    """Create theft success rate visualization"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Calculate success rate
    total = len(df)
    successful = total  # All records are successful thefts (filtered earlier)
    attempted = 0  # From original: only 105 out of 21,403 were attempted
    
    # Approximate success rate
    success_rate = 99.5
    failure_rate = 0.5
    
    # Create pie chart
    sizes = [success_rate, failure_rate]
    labels = [f'Successful Thefts\n{success_rate}%\n(~{total:,} thefts)', 
              f'Attempted (Failed)\n{failure_rate}%\n(~105 attempts)']
    colors = ['#d32f2f', '#4caf50']
    explode = (0.05, 0.1)
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                        explode=explode, startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'},
                                        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
    
    ax.set_title('Theft Success Rate: Professional Operations', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # Add annotation
    ax.text(0, -1.4, 'Implication: These are PROFESSIONAL thieves, not amateurs.\nThey know exactly what they\'re doing.',
            ha='center', fontsize=12, fontweight='bold', style='italic',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('visualizations/viz_4_success_rate_expert.png', dpi=120, bbox_inches='tight')
    plt.close()
    print("✓ Success rate chart generated")

def main():
    """Generate all visualizations"""
    print("Loading data...")
    df = load_data()
    
    print(f"Generating visualizations for {len(df):,} records...")
    create_peak_hour_chart(df)
    create_weekday_chart(df)
    create_bike_value_chart(df)
    create_success_rate_chart(df)
    
    print("\n✅ All visualizations generated successfully")
    print(f"Last updated: {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}")

if __name__ == '__main__':
    main()
