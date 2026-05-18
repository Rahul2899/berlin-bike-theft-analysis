"""
Create slow, professional MP4 video animations from analysis data
High-quality animations suitable for LinkedIn
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation, FFMpegWriter
import numpy as np
import os

# Ensure output directory exists
os.makedirs('visualizations', exist_ok=True)

def load_data(data_path='data/processed/geocoded_data.csv'):
    """Load cleaned dataset"""
    return pd.read_csv(data_path)

def create_slow_peak_hours_video(df, output_file='visualizations/peak_hours_animation.mp4'):
    """Create slow, professional peak hours animation"""
    print("Creating peak hours animation (slow, 60 seconds)...")
    
    # Calculate hourly thefts
    hourly = df['incident_hour'].value_counts().sort_index()
    hours = hourly.index.values
    counts = hourly.values
    max_count = counts.max()
    
    fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
    
    # Total frames = 240 (4 seconds per hour animation at 30fps = 120 frames total + 60 extra for pause)
    total_frames = 240
    
    def animate(frame):
        ax.clear()
        
        # Progress through hours slowly
        progress = frame / total_frames
        current_hour_index = int(progress * len(hours))
        
        if current_hour_index >= len(hours):
            current_hour_index = len(hours) - 1
        
        current_hours = hours[:current_hour_index+1]
        current_counts = counts[:current_hour_index+1]
        
        # Color mapping: gradient from light to dark red as bars grow
        colors = []
        for i, count in enumerate(current_counts):
            ratio = count / max_count
            if ratio > 0.8:
                colors.append('#d32f2f')  # Bright red for peak
            elif ratio > 0.6:
                colors.append('#e53935')  # Red
            elif ratio > 0.4:
                colors.append('#ff6f00')  # Orange
            else:
                colors.append('#ffa726')  # Light orange
        
        bars = ax.bar(current_hours, current_counts, color=colors, edgecolor='black', linewidth=1.5)
        
        # Add value labels on top of bars
        for bar, count in zip(bars, current_counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(count):,}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Formatting with larger fonts
        ax.set_xlabel('Hour of Day (24h)', fontsize=18, fontweight='bold')
        ax.set_ylabel('Number of Bike Thefts', fontsize=18, fontweight='bold')
        ax.set_title('When Do Thieves Strike? Hour-by-Hour Analysis', 
                    fontsize=22, fontweight='bold', pad=30)
        ax.set_xlim(-0.5, 23.5)
        ax.set_ylim(0, max_count * 1.15)
        ax.set_xticks(range(0, 24, 2))
        ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1)
        
        # Current hour indicator
        if current_hour_index < len(hours):
            current_hour = int(hours[current_hour_index])
            current_count = int(current_counts[current_hour_index])
            
            ax.text(0.02, 0.95, f'Hour: {current_hour:02d}:00\nThefts: {current_count:,}',
                   transform=ax.transAxes, fontsize=16, fontweight='bold',
                   verticalalignment='top',
                   bbox=dict(boxstyle='round,pad=1', facecolor='yellow', alpha=0.8, linewidth=2))
        
        # Peak indicator
        peak_idx = np.argmax(counts)
        ax.text(0.98, 0.95, f'PEAK: {int(hours[peak_idx])}:00\n{int(counts[peak_idx]):,} thefts',
               transform=ax.transAxes, fontsize=16, fontweight='bold', color='#d32f2f',
               verticalalignment='top', horizontalalignment='right',
               bbox=dict(boxstyle='round,pad=1', facecolor='#ffebee', alpha=0.9, linewidth=2))
    
    anim = FuncAnimation(fig, animate, frames=total_frames, repeat=False, interval=1000/30)
    
    # Save as MP4 at 30fps
    try:
        writer = FFMpegWriter(fps=30, bitrate=2000, codec='libx264')
        anim.save(output_file, writer=writer, dpi=100)
        print(f"✓ Peak hours video saved: {output_file}")
        return True
    except Exception as e:
        print(f"⚠️  MP4 creation failed: {e}. Trying GIF instead...")
        return False
    finally:
        plt.close()

def create_slow_weekday_video(df, output_file='visualizations/weekday_animation.mp4'):
    """Create slow, professional weekday comparison animation"""
    print("Creating weekday comparison animation (slow, 45 seconds)...")
    
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily = df['day_of_week'].value_counts().reindex(weekday_order)
    
    fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
    
    # Total frames = 180 (slow reveal, 6 seconds per day at 30fps)
    total_frames = 180
    
    def animate(frame):
        ax.clear()
        
        # Progress through days slowly
        progress = frame / total_frames
        current_day_index = int(progress * len(weekday_order))
        
        if current_day_index >= len(weekday_order):
            current_day_index = len(weekday_order) - 1
        
        days_to_show = weekday_order[:current_day_index+1]
        counts_to_show = daily.values[:current_day_index+1]
        
        # Colors: weekdays orange, weekends blue
        colors = ['#ff6f00' if day not in ['Saturday', 'Sunday'] else '#1976d2' for day in days_to_show]
        
        bars = ax.bar(range(len(counts_to_show)), counts_to_show, color=colors, 
                     edgecolor='black', linewidth=2)
        
        # Add value labels with large font
        for bar, count in zip(bars, counts_to_show):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(count):,}', ha='center', va='bottom', fontsize=13, fontweight='bold')
        
        ax.set_xticks(range(len(days_to_show)))
        ax.set_xticklabels(days_to_show, rotation=45, ha='right', fontsize=14, fontweight='bold')
        ax.set_ylabel('Number of Bike Thefts', fontsize=18, fontweight='bold')
        ax.set_title('The Weekday Effect: When Are Your Bikes Most Vulnerable?', 
                    fontsize=22, fontweight='bold', pad=30)
        ax.set_ylim(0, daily.values.max() * 1.25)
        ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1)
        
        # Show current statistics
        if current_day_index == len(weekday_order) - 1:
            weekday_total = daily[:'Friday'].sum()
            weekend_total = daily['Saturday':].sum()
            ratio = weekday_total / weekend_total
            
            ax.text(0.5, -0.25, f'WEEKDAYS: {int(weekday_total):,} thefts | WEEKENDS: {int(weekend_total):,} thefts | RATIO: {ratio:.1f}x',
                   transform=ax.transAxes, fontsize=16, fontweight='bold',
                   ha='center', bbox=dict(boxstyle='round,pad=1', facecolor='yellow', alpha=0.8, linewidth=2))
    
    anim = FuncAnimation(fig, animate, frames=total_frames, repeat=False, interval=1000/30)
    
    try:
        writer = FFMpegWriter(fps=30, bitrate=2000, codec='libx264')
        anim.save(output_file, writer=writer, dpi=100)
        print(f"✓ Weekday comparison video saved: {output_file}")
        return True
    except Exception as e:
        print(f"⚠️  MP4 creation failed: {e}. Trying GIF instead...")
        return False
    finally:
        plt.close()

def main():
    """Generate all video animations"""
    print("Loading data...")
    df = load_data()
    
    print(f"Generating professional videos for {len(df):,} records...\n")
    
    peak_success = create_slow_peak_hours_video(df)
    weekday_success = create_slow_weekday_video(df)
    
    if peak_success and weekday_success:
        print("\n✅ All MP4 videos created successfully!")
        print("Videos are high-quality, slow, and ready for LinkedIn")
        print("Files saved to visualizations/ folder (MP4 format)")
    else:
        print("\n⚠️  Some videos failed. Check FFmpeg installation.")

if __name__ == '__main__':
    main()
