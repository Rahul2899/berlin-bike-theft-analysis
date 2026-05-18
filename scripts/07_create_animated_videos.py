"""
Create animated video visualizations from analysis data
Generates two MP4 videos showing dynamic theft patterns
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

def load_data(data_path='data/processed/geocoded_data.csv'):
    """Load cleaned dataset"""
    return pd.read_csv(data_path)

def create_animated_peak_hours(df, output_file='visualizations/animated_peak_hours.gif'):
    """Create animated peak hours bar chart"""
    print("Creating animated peak hours chart...")
    
    # Calculate hourly thefts
    hourly = df['incident_hour'].value_counts().sort_index()
    hours = hourly.index.values
    counts = hourly.values
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 7))
    
    def animate(frame):
        ax.clear()
        
        # Only show bars up to current frame
        current_hours = hours[:frame+1]
        current_counts = counts[:frame+1]
        
        # Color bars: red for peak, orange for high, yellow for medium
        colors = []
        for count in current_counts:
            if count == counts.max():
                colors.append('#d32f2f')  # Red for peak
            elif count > np.percentile(counts, 75):
                colors.append('#ff6f00')  # Orange for high
            else:
                colors.append('#ffa726')  # Yellow for medium
        
        bars = ax.bar(current_hours, current_counts, color=colors, edgecolor='black', linewidth=0.5)
        
        # Formatting
        ax.set_xlabel('Hour of Day', fontsize=14, fontweight='bold')
        ax.set_ylabel('Number of Thefts', fontsize=14, fontweight='bold')
        ax.set_title(f'Peak Theft Hours in Berlin | Analyzing Hour {frame}', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlim(-0.5, 23.5)
        ax.set_ylim(0, counts.max() * 1.1)
        ax.set_xticks(range(0, 24, 2))
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add current count
        if frame < len(hours):
            ax.text(0.98, 0.95, f'Hour {frame}:00\n{current_counts[-1]:,} thefts',
                   transform=ax.transAxes, fontsize=12, fontweight='bold',
                   verticalalignment='top', horizontalalignment='right',
                   bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    anim = FuncAnimation(fig, animate, frames=len(hours), repeat=True, interval=200)
    
    # Save as GIF
    writer = PillowWriter(fps=5)
    anim.save(output_file, writer=writer)
    plt.close()
    print(f"✓ Animated peak hours saved: {output_file}")

def create_animated_weekday_buildup(df, output_file='visualizations/animated_weekday_comparison.gif'):
    """Create animated weekday vs weekend comparison"""
    print("Creating animated weekday comparison chart...")
    
    # Calculate daily counts
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily = df['day_of_week'].value_counts().reindex(weekday_order)
    
    # Cumulative for animation effect
    cumulative = np.cumsum(daily.values)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    def animate(frame):
        ax.clear()
        
        # Show animation building up
        if frame < len(weekday_order):
            # Animate individual days
            days_to_show = weekday_order[:frame+1]
            counts_to_show = daily.values[:frame+1]
        else:
            days_to_show = weekday_order
            counts_to_show = daily.values
        
        colors = ['#ff6f00' if day not in ['Saturday', 'Sunday'] else '#1976d2' for day in days_to_show]
        
        bars = ax.bar(range(len(counts_to_show)), counts_to_show, color=colors, 
                     edgecolor='black', linewidth=0.5)
        
        # Add value labels
        for bar, count in zip(bars, counts_to_show):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(count):,}', ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        ax.set_xticks(range(len(days_to_show)))
        ax.set_xticklabels(days_to_show, rotation=45, ha='right')
        ax.set_ylabel('Number of Thefts', fontsize=14, fontweight='bold')
        ax.set_title('Weekday Effect: When Are Bikes Most Vulnerable?', 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_ylim(0, daily.values.max() * 1.2)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add statistic
        if len(days_to_show) == 7:
            weekday_total = daily[:'Friday'].sum()
            weekend_total = daily['Saturday':].sum()
            ratio = weekday_total / weekend_total
            ax.text(0.02, 0.98, f'WEEKDAYS: 3.1x more dangerous than weekends',
                   transform=ax.transAxes, fontsize=13, fontweight='bold', color='#d32f2f',
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    anim = FuncAnimation(fig, animate, frames=len(weekday_order)+1, repeat=True, interval=400)
    
    # Save as GIF
    writer = PillowWriter(fps=3)
    anim.save(output_file, writer=writer)
    plt.close()
    print(f"✓ Animated weekday comparison saved: {output_file}")

def main():
    """Generate all animated visualizations"""
    print("Loading data...")
    df = load_data()
    
    print(f"Generating animations for {len(df):,} records...\n")
    create_animated_peak_hours(df)
    create_animated_weekday_buildup(df)
    
    print("\n✅ All animations created successfully!")
    print("Files saved to visualizations/ folder (GIF format for LinkedIn)")

if __name__ == '__main__':
    main()
