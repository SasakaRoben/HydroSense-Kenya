import pandas as pd
import numpy as np

weather = pd.read_csv('../data/raw/weather_daily.csv', 
                            na_values=['NA', ''])
soil = pd.read_csv('../data/raw/soil_sensor_data.csv', 
                              na_values=['NA', ''])
params = pd.read_csv('../data/raw/crop_zone_parameters.csv', 
                                  na_values=['NA', ''])

weather_clean = weather.copy()

# Fix missing continuous values (Rainfall and Humidity) via linear interpolation
weather_clean['rainfall_mm'] = weather_clean['rainfall_mm'].interpolate(method='linear')
weather_clean['humidity_pct'] = weather_clean['humidity_pct'].interpolate(method='linear')

# Isolate, mask, and interpolate the temperature sensor spike (45.8°C)
weather_clean.loc[weather_clean['temperature_c'] > 35, 'temperature_c'] = np.nan
weather_clean['temperature_c'] = weather_clean['temperature_c'].interpolate(method='linear')


soil_clean = soil.copy()

# Impute missing soil moisture within its respective crop zone sequence
soil_clean['soil_moisture_pct'] = soil_clean.groupby('zone_id')['soil_moisture_pct'].transform(
    lambda x: x.interpolate(method='linear')
)

# Identify and mask the arbitrary tank telemetry surge (9900 Liters)
soil_clean.loc[soil_clean['tank_level_liters'] > 5500, 'tank_level_liters'] = np.nan
soil_clean['tank_level_liters'] = soil_clean.groupby('zone_id')['tank_level_liters'].transform(
    lambda x: x.interpolate(method='linear')
)

# Address the logical telemetry contradiction (Pump running at 468W but flow reads 0.0 lpm)
# Calculate the standard operational flow rate for Zone B pumps
zone_b_active_flow = soil_clean[(soil_clean['zone_id'] == 'Zone_B') & (soil_clean['pump_flow_lpm'] > 0)]['pump_flow_lpm'].mean()

# Apply standard flow and adjust flag status on the faulty entry
contradiction_mask = (soil_clean['sensor_status'] == 'CHECK') & (soil_clean['pump_flow_lpm'] == 0)
soil_clean.loc[contradiction_mask, 'pump_flow_lpm'] = round(zone_b_active_flow, 1)
soil_clean.loc[contradiction_mask, 'sensor_status'] = 'CLEANED'


weather_clean.to_csv('../data/processed/weather_daily_cleaned.csv', index=False)
soil_clean.to_csv('../data/processed/soil_sensor_data_cleaned.csv', index=False)