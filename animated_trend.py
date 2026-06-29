# animated_trend.py
# Creates an animated trend graph (GIF)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os


print("CREATING ANIMATED TREND GRAPH")

# Load Data
# ============================================
print("\n[1] Loading data...")

df = pd.read_csv("cleaned_data.csv")
print(f"   Loaded: {len(df)} rows")

# Identify Fuel Column
# ============================================
fuel_col = 'EngFuelRate_(L/h)'
print(f"   Fuel: {fuel_col}")

# Get Data for Animation (First 500 points)
# ============================================
data = df[[fuel_col]].dropna().iloc[:500, :]
x = np.arange(len(data))
y = data[fuel_col].values

# Calculate trend line
slope, intercept, r, p, _ = stats.linregress(x, y)
trend_line = slope * x + intercept

print(f"   Using {len(x)} data points")

# Create Frames for Animation
# ============================================
print("\n[2] Creating animation frames...")

# Create a folder for frames
os.makedirs("frames", exist_ok=True)

frames = []
step_size = 20  # Number of points to add each frame

for i in range(step_size, len(x) + step_size, step_size):
    # Limit to the current step
    current_x = x[:i]
    current_y = y[:i]
    current_trend = trend_line[:i]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot the data up to current point
    ax.plot(current_x, current_y, 'b-', linewidth=2, alpha=0.8, label='Fuel Consumption')
    
    # Plot the trend line
    ax.plot(current_x, current_trend, 'r--', linewidth=2, alpha=0.6, label=f'Trend (r={r:.3f})')
    
    # Fill under the line
    ax.fill_between(current_x, current_y, y.min() - 1, alpha=0.15, color='blue')
    
    # Title with progress
    progress = int((i / len(x)) * 100)
    ax.set_title(f'Tractor Fuel Consumption Trend (Loading: {progress}%)', 
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Data Point Index')
    ax.set_ylabel('Fuel Consumption (L/h)')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(y.min() - 1, y.max() + 1)
    
    # Save frame
    frame_path = f"frames/frame_{i:04d}.png"
    plt.savefig(frame_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    frames.append(frame_path)
    print(f"   Frame {len(frames)}: {progress}% complete")

# Create GIF using PIL
# ============================================
print("\n[3] Creating animated GIF...")

from PIL import Image

images = []
for frame in frames:
    img = Image.open(frame)
    images.append(img)

# Save as GIF
gif_path = "trend_animation.gif"
images[0].save(gif_path, save_all=True, append_images=images[1:], duration=200, loop=0)
print(f" Saved: {gif_path}")

# Clean Up Frames
# ============================================
print("\n[4] Cleaning up temporary frames...")
import shutil
shutil.rmtree("frames")
print("Frames deleted")

print("\n" + "=" * 60)
print("ANIMATED TREND GRAPH COMPLETE!")
print(f"   File: {gif_path}")
print("   Open the GIF in your browser to see the animation.")
print("=" * 60)