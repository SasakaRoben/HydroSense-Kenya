import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gamma

# ==========================================================
# 1. LOAD DATA AND EXTRACT STATISTICAL PROPERTIES
# ==========================================================
# Read the project dataset
df = pd.read_csv("../data/processed/weather_daily_cleaned.csv")
df['rainfall_mm'] = pd.to_numeric(df['rainfall_mm'], errors='coerce').fillna(0.0)

# Isolate days when it actually rained to calibrate our wet-day distribution
wet_days = df[df['rainfall_mm'] > 0.1]['rainfall_mm'].values

# Calculate empirical probabilities
total_days = len(df)
rain_probability = len(wet_days) / total_days  # Likelihood of any given day being rainy

# Fit a Gamma distribution to the historical wet-day data to find shape parameters
# shape (alpha) controls the peak, scale (beta) controls the tail length
shape_fit, loc_fit, scale_fit = gamma.fit(wet_days, floc=0)

# ==========================================================
# 2. MONTE CARLO SIMULATION ENGINE
# ==========================================================
NUM_SCENARIOS = 1000   # Number of parallel realities to simulate
FORECAST_DAYS = 30     # Timeline window length

# Seed the generator for mathematical reproducibility
np.random.seed(42)

# Matrix structure to hold simulation data: 30 rows (days) by 1000 columns (scenarios)
simulated_rainfall_matrix = np.zeros((FORECAST_DAYS, NUM_SCENARIOS))

for scenario in range(NUM_SCENARIOS):
    for day in range(FORECAST_DAYS):
        # Step A: Roll a random number to determine if it rains at all
        if np.random.rand() < rain_probability:
            # Step B: If rainy, sample an intensity value from the calibrated Gamma curve
            simulated_rainfall_matrix[day, scenario] = gamma.rvs(shape_fit, loc=loc_fit, scale=scale_fit)
        else:
            simulated_rainfall_matrix[day, scenario] = 0.0

# Calculate cumulative rainfall tracks across the month for each scenario
cumulative_tracks = np.cumsum(simulated_rainfall_matrix, axis=0)

# ==========================================================
# 3. GENERATE RISK ANALYSIS AND GRAPH
# ==========================================================
plt.figure(figsize=(12, 6))

# Plot all 1,000 Monte Carlo paths with high transparency (alpha) to see density
plt.plot(range(1, FORECAST_DAYS + 1), cumulative_tracks, color='gray', alpha=0.08)

# Calculate key statistical percentiles for risk boundaries
p10_drought = np.percentile(cumulative_tracks[-1, :], 10)
p50_median  = np.percentile(cumulative_tracks[-1, :], 50)
p90_flood   = np.percentile(cumulative_tracks[-1, :], 90)

# Highlight explicit risk pathways on the graph
plt.plot(range(1, FORECAST_DAYS + 1), np.median(cumulative_tracks, axis=1), 
         color='blue', linewidth=2.5, label=f'Median Scenario (P50: {p50_median:.1f} mm)')
plt.plot(range(1, FORECAST_DAYS + 1), np.percentile(cumulative_tracks, q=90, axis=1), 
         color='red', linewidth=2, linestyle='--', label=f'Worst-Case Flood Risk (P90: {p90_flood:.1f} mm)')
plt.plot(range(1, FORECAST_DAYS + 1), np.percentile(cumulative_tracks, q=10, axis=1), 
         color='orange', linewidth=2, linestyle='--', label=f'Severe Drought Risk (P10: {p10_drought:.1f} mm)')

plt.title(f"Monte Carlo Risk Analysis: 1,000 Cumulative Rainfall Uncertainty Scenarios", fontsize=13, fontweight='bold')
plt.xlabel("Forecast Timeline (Days)", fontsize=11)
plt.ylabel("Cumulative Simulated Rainfall (mm)", fontsize=11)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc="upper left", fontsize=10)
plt.tight_layout()
plt.show()

# Print Risk Dashboard
print("=" * 55)
print(f"{'MONTE CARLO HYDROLOGICAL RISK REPORT':^55}")
print("=" * 55)
print(f"Historical Rain Probability per Day : {rain_probability*100:.2f}%")
print(f"Calibrated Gamma Shape Factor (α)   : {shape_fit:.4f}")
print(f"Calibrated Gamma Scale Factor (β)   : {scale_fit:.4f}")
print("-" * 55)
print(f"10th Percentile (Severe Drought Risk): {p10_drought:.2f} mm total")
print(f"50th Percentile (Expected Median)    : {p50_median:.2f} mm total")
print(f"90th Percentile (Severe Flood Risk)  : {p90_flood:.2f} mm total")
print("=" * 55)