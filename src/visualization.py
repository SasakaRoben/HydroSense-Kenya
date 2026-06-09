import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned datasets
weather = pd.read_csv('../data/processed/weather_daily_cleaned.csv')
soil = pd.read_csv('../data/processed/soil_sensor_data_cleaned.csv')
crop = pd.read_csv('../data/processed/crop_zone_parameters_cleaned.csv')

# Parse dates
weather['date'] = pd.to_datetime(weather['date'])
soil['timestamp'] = pd.to_datetime(soil['timestamp'])
soil['date'] = soil['timestamp'].dt.date
soil['date'] = pd.to_datetime(soil['date'])

# Set seaborn style for publication-quality visuals
# sns.set_theme(style="whitegrid", context="talk")

# 1. Visualization 1: Soil Moisture Dynamics vs. Crop Management Thresholds
fig, axes = plt.subplots(3, 1, figsize=(12, 14), sharex=True)
zones = ['Zone_A', 'Zone_B', 'Zone_C']
colors = ['#e41a1c', '#4daf4a', '#377eb8']

for i, zone in enumerate(zones):
    zone_soil = soil[soil['zone_id'] == zone].sort_values('date')
    zone_crop = crop[crop['zone_id'] == zone].iloc[0]
    
    axes[i].plot(zone_soil['date'], zone_soil['soil_moisture_pct'], marker='o', color=colors[i], linewidth=2.5, label=f"Observed Moisture ({zone_crop['crop_type'].capitalize()})")
    axes[i].axhline(zone_crop['target_moisture_pct'], color='green', linestyle='--', linewidth=1.5, label=f"Target ({zone_crop['target_moisture_pct']}%)")
    axes[i].axhline(zone_crop['min_moisture_pct'], color='orange', linestyle='-.', linewidth=1.5, label=f"Min Critical ({zone_crop['min_moisture_pct']}%)")
    axes[i].axhline(zone_crop['field_capacity_pct'], color='blue', linestyle=':', linewidth=1.5, label=f"Field Capacity ({zone_crop['field_capacity_pct']}%)")
    
    axes[i].set_ylabel("Soil Moisture (%)", fontsize=14)
    axes[i].set_title(f"{zone} - Crop: {zone_crop['crop_type'].capitalize()}", fontsize=16, fontweight='bold')
    axes[i].legend(loc='lower left', fontsize=11, frameon=True)
    axes[i].set_ylim(5, 50)

axes[2].set_xlabel("Timeline (March 2026)", fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('vis1_soil_moisture_thresholds.png', dpi=150)
plt.close()

# 2. Visualization 2: Pump Hydromechanical Performance Curve
fig, ax = plt.subplots(figsize=(10, 6))
for i, zone in enumerate(zones):
    zone_soil = soil[soil['zone_id'] == zone]
    sns.regplot(data=zone_soil, x='pump_power_watts', y='pump_flow_lpm', ax=ax, label=f"{zone} Pumps", 
                color=colors[i], scatter_kws={'s': 60, 'alpha': 0.7}, line_kws={'linewidth': 2})

ax.set_title("Pump Performance Characteristic Curves:\nVolumetric Flow Rate vs. Electrical Power Consumption", fontsize=16, fontweight='bold')
ax.set_xlabel("Pump Power Consumption (Watts)", fontsize=14)
ax.set_ylabel("Pump Flow Rate (Liters per Minute)", fontsize=14)
ax.legend(loc='best', fontsize=12)
plt.tight_layout()
plt.savefig('vis2_pump_performance.png', dpi=150)
plt.close()

# 3. Visualization 3: Microclimatic Evaporative Demand Drivers (VPD Proxies)
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(weather['temperature_c'], weather['humidity_pct'], c=weather['solar_index'], 
                     cmap='YlOrRd', s=weather['wind_speed_mps']*40, alpha=0.8, edgecolor='w', linewidth=0.5)

cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Solar Index (Irradiance Proxy)', fontsize=12)
ax.set_title("Microclimatic Evaporative Drivers:\nTemperature vs. Humidity Modulated by Solar Radiation & Wind Speed", fontsize=16, fontweight='bold')
ax.set_xlabel("Ambient Temperature (°C)", fontsize=14)
ax.set_ylabel("Relative Humidity (%)", fontsize=14)

# Create a legend for wind speed sizes
kw = dict(prop="sizes", num=4, color="grey", fmt="{x:.1f} m/s", func=lambda s: s/40)
legend2 = ax.legend(*scatter.legend_elements(**kw), loc="upper right", title="Wind Speed")
ax.add_artist(legend2)

plt.tight_layout()
plt.savefig('vis3_microclimate_drivers.png', dpi=150)
plt.close()

# 4. Visualization 4: Soil Hydrodynamics & Moisture Response to Precipitation
fig, ax1 = plt.subplots(figsize=(12, 6))

# Calculate daily mean soil moisture across all zones to see the macro trend
daily_avg_moisture = soil.groupby('date')['soil_moisture_pct'].mean().reset_index()

ax1.plot(daily_avg_moisture['date'], daily_avg_moisture['soil_moisture_pct'], color='#2b8cbe', linewidth=3, marker='s', label='Mean Soil Moisture (%)')
ax1.set_xlabel('Timeline (March 2026)', fontsize=14)
ax1.set_ylabel('Mean Soil Moisture (%)', color='#2b8cbe', fontsize=14)
ax1.tick_params(axis='y', labelcolor='#2b8cbe')
ax1.set_ylim(15, 35)

ax2 = ax1.twinx()
ax2.bar(weather['date'], weather['rainfall_mm'], alpha=0.3, color='#a6cee3', width=0.6, label='Daily Rainfall (mm)')
ax2.set_ylabel('Daily Rainfall (mm)', color='#1f78b4', fontsize=14)
ax2.tick_params(axis='y', labelcolor='#1f78b4')
ax2.set_ylim(0, 100)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

plt.title("Soil Hydrodynamics: Ecosystem-Scale Soil Moisture Response\nto Meteoric Precipitation Events", fontsize=16, fontweight='bold')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('vis4_soil_hydrodynamics.png', dpi=150)
plt.close()

# 5. Visualization 5: Crop-Specific Soil Moisture Distribution & Physiological Compliance
fig, ax = plt.subplots(figsize=(10, 6))
# Use `hue` with the same grouping and disable the legend to satisfy seaborn's API (avoids FutureWarning)
sns.boxplot(data=soil, x='zone_id', y='soil_moisture_pct', hue='zone_id', palette=colors, ax=ax, width=0.5, fliersize=6, legend=False)

# Overlay individual zone parameters for context
for i, zone in enumerate(zones):
    zc = crop[crop['zone_id'] == zone].iloc[0]
    # Add labels or markers for target and min moisture
    ax.plot([i-0.25, i+0.25], [zc['target_moisture_pct'], zc['target_moisture_pct']], color='green', linestyle='--', linewidth=2)
    ax.plot([i-0.25, i+0.25], [zc['min_moisture_pct'], zc['min_moisture_pct']], color='orange', linestyle='-.', linewidth=2)
    ax.plot([i-0.25, i+0.25], [zc['field_capacity_pct'], zc['field_capacity_pct']], color='blue', linestyle=':', linewidth=2)

# Custom legend entries for lines
from matplotlib.lines import Line2D
custom_lines = [Line2D([0], [0], color='green', linestyle='--', linewidth=2),
                Line2D([0], [0], color='orange', linestyle='-.', linewidth=2),
                Line2D([0], [0], color='blue', linestyle=':', linewidth=2)]
ax.legend(custom_lines, ['Crop Target', 'Min Critical', 'Field Capacity'], loc='lower left', fontsize=11)

ax.set_title("Crop-Specific Soil Moisture Distribution\nand Physiological Boundary Compliance", fontsize=16, fontweight='bold')
ax.set_xlabel("Agricultural Zone / Managed Crop Type", fontsize=14)
ax.set_ylabel("Soil Moisture Percentage (%)", fontsize=14)
# Ensure tick positions are fixed before setting labels to avoid UserWarning
ax.set_xticks(list(range(len(zones))))
ax.set_xticklabels(["Zone A\n(Tomato)", "Zone B\n(Kale)", "Zone C\n(Maize)"])

plt.tight_layout()
plt.savefig('vis5_physiological_compliance.png', dpi=150)
plt.close()