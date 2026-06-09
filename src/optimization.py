import pandas as pd
import numpy as np

# ==========================================================
# 1. LOAD AND CLEAN TARGET WEATHER DATASET
# ==========================================================
df_weather = pd.read_csv("weather_daily.csv", parse_dates=['date'])
df_weather['rainfall_mm'] = pd.to_numeric(df_weather['rainfall_mm'], errors='coerce').fillna(0.0)
df_weather['temperature_c'] = pd.to_numeric(df_weather['temperature_c'], errors='coerce').fillna(24.0)
df_weather['humidity_pct'] = pd.to_numeric(df_weather['humidity_pct'], errors='coerce').fillna(65.0)

# ==========================================================
# 2. DEFINE IRRIGATION SCHEDULING CONSTRAINTS
# ==========================================================
WILTING_POINT   = 25.0   # Critical crop stress line (%)
MAD_TRIGGER     = 28.0   # Managed Allowed Depletion trigger point (%)
TARGET_MOISTURE = 38.0   # Efficient refill ceiling (%)
CONVERSION_FAC  = 0.45   # 1 mm of net water adds 0.45% moisture

# Initialize tracking vectors
moisture_log = [33.20]  # Starting condition matching Zone_A baseline
irrigation_schedule = []

# ==========================================================
# 3. RUN SIMULATION LOOP WITH CONSERVATION SCHEDULING
# ==========================================================
for i in range(len(df_weather)):
    current_moisture = moisture_log[-1]
    
    # Fetch real-world environmental data for the current day
    rain = df_weather.loc[i, 'rainfall_mm']
    temp = df_weather.loc[i, 'temperature_c']
    hum  = df_weather.loc[i, 'humidity_pct']
    
    # Calculate natural system dynamics
    I = rain * 0.45
    ET = 2.5 * (temp / 25.0) * (1.0 - (hum / 100.0))
    DP = 0.04 * current_moisture
    
    # Step 1: Predict soil state after natural environmental forcing
    predicted_moisture = current_moisture + (I - ET - DP)
    
    # Step 2: Evaluate scheduling rule
    # If the predicted moisture drops below our MAD safety line...
    if predicted_moisture <= MAD_TRIGGER:
        # Calculate precise moisture deficit needed to reach the target ceiling
        moisture_deficit = TARGET_MOISTURE - predicted_moisture
        
        # Convert the percentage deficit directly into required water depth (mm)
        required_irrigation_mm = moisture_deficit / CONVERSION_FAC
        
        # Execute irrigation pulse
        applied_irrigation = required_irrigation_mm
        final_moisture = TARGET_MOISTURE
    else:
        # No watering required; let natural variables govern the state
        applied_irrigation = 0.0
        final_moisture = predicted_moisture
        
    # Enforce global physical saturation cap
    final_moisture = max(0.0, min(100.0, final_moisture))
    
    # Log results for reporting
    moisture_log.append(final_moisture)
    irrigation_schedule.append({
        'Date': df_weather.loc[i, 'date'].strftime('%Y-%m-%d'),
        'Pre-Irrigation Moisture (%)': predicted_moisture,
        'Natural Rainfall (mm)': rain,
        'Scheduled Irrigation (mm)': applied_irrigation,
        'Post-Irrigation Moisture (%)': final_moisture
    })

# Drop initialization padding from tracking log
moisture_log = moisture_log[:-1]
df_schedule = pd.DataFrame(irrigation_schedule)