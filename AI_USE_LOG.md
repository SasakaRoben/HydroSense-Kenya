# AI Use Log: HydroSense-Kenya Capstone Project

This log maintains a transparent, auditable record of AI assistance utilized for software engineering, numerical analysis, and simulation tasks in the ICS 2207 Scientific Computing course.



## [LOG-001] Finite Difference Implementation
* **Date:** 2026-03-05
* **Task Context:** Module 1 – Data Cleaning and Numerical Differentiation

### 1. Initial Prompt
> "Change this code to use the dataset in the picture... [Code block with hardcoded 1D lists for hourly volumetric soil-moisture profile]"

### 2. Generated AI Output
* Provided a script utilizing `pandas` to recreate a slice of `soil_sensor_data.csv`.
* Filtered by `zone_id == 'Zone_A'` to maintain time-series integrity.
* Hardcoded step size to $h = 24.0$ hours matching daily noon intervals.
* Provided explicit `for` loop iteration with `pd.isna()` boundaries to safeguard against the deliberate missing data anomalies (`NA` values).

### 3. Applied Modifications
* **Code Translation:** Replaced the hardcoded dictionary array with a direct CSV file pipeline (`pd.read_csv("soil_sensor_data.csv")`) as requested in follow-up tasks.
* **Optimization:** Shifted the explicit looping logic to high-performance pandas vectorization using `.shift(1)` and `.shift(-1)` to calculate the central, forward, and backward differences efficiently.

### 4. Verification & Validation Methods
* **Boundary Check:** Verified that boundary indices (`Index 0` and `Index 29`) correctly evaluated to `NaN` or `N/A` matching physical constraints.
* **Mathematical Verification:** Hand-calculated `Index 2` (`2026-03-03`):
  $$\text{Central Diff} = \frac{31.8 - 36.1}{2 \times 24} = -0.089583\% \text{/hr}$$
  Cross-checked this value against the terminal dataframe printout to guarantee algorithmic accuracy.



## [LOG-002] Multi-Method Hydrological Integration
* **Date:** 2026-03-12
* **Task Context:** Module 2 – Cumulative Rainfall Integration (`weather_daily.csv`)

### 1. Initial Prompt
> "Change this to use my dataset, or simulation doesn't require a dataset? [Code block containing baseline Trapezoidal and Simpson's 1/3 rules with hardcoded arrays]"

### 2. Generated AI Output
* Created an anomaly-resilient parsing engine for `weather_daily.csv`.
* Implemented a composite mathematical wrapper: detects odd total intervals ($n=29$), integrates the first 28 via Simpson's 1/3 rule, and evaluates the final odd tail slice via a Trapezoidal patch.

### 3. Applied Modifications
* Adjusted the missing value handler from a flat `.dropna()` configuration to a conditional `.fillna(0.0)` for the `rainfall_mm` column. Dropping rows entirely would corrupt the uniform step size ($h = 1.0\text{ day}$), breaking the integration constraints.

### 4. Verification & Validation Methods
* **Method Benchmarking:** Ran independent executions of a pure Trapezoidal integration versus the Composite Simpson's Mix. 
* **Discrepancy Audit:** Logged a baseline difference of $20.5667\text{ mm}$ ($245.350\text{ mm}$ vs $265.917\text{ mm}$). Validated that this variance was mathematically reasonable due to Simpson's second-order parabolic curve catching the true peak area of the $85.00\text{ mm}$ storm event on March 26th much better than linear trapezoids.



## [LOG-003] Predictive Euler vs. RK4 Simulation
* **Date:** 2026-03-20
* **Task Context:** Module 3 – Predictive Modeling & Uncertainty Analysis

### 1. Initial Prompt
> "Explain the Runge Kutta method and repeat the simulation using the Runge Kutta method and compare with the Euler method"

### 2. Generated AI Output
* Formulated the multi-step mathematical engines for 1st-Order Euler and 4th-Order Runge-Kutta (RK4).
* Structured a continuous tracking loop driven by three dynamic forcing metrics mapped directly from the daily weather series data: Infiltration ($I$), Evapotranspiration ($ET$), and Deep Percolation ($DP$).

### 3. Applied Modifications
* Added a hard boundary truncation layer (`max(0.0, min(100.0, theta_next))`) to both simulation paths. Without this limit, consecutive extreme rain forcing could push soil moisture past $100\%$ physical saturation limits.

### 4. Verification & Validation Methods
* **Visual Calibration Plotting:** Plotted both models against actual observed field sensor values for `Zone_A`.
* **Sensitivity Analysis:** Identified that under a 1-day step size ($h=1.0$), both numerical solvers yielded identical curves because the strong daily weather forcing data dominated the system over the subtle mathematical truncation differences.



## [LOG-004] Stochastic Risk Engine (Monte Carlo)
* **Date:** 2026-03-28
* **Task Context:** Module 4 – Optimization and Operational Risk Planning

### 1. Initial Prompt
> "Design an irrigation schedule that minimizes water use while keeping moisture above the minimum threshold."

### 2. Generated AI Output
* Developed a 1,000-trial Monte Carlo loop calibrating rainfall volatility to a non-negative Gamma probability distribution.
* Created a Managed Allowed Depletion (MAD) smart-scheduling algorithm triggering irrigation refiles to an upper limit of $38\%$.

### 3. Applied Modifications
* Advanced the irrigation trigger threshold from the absolute crop wilting limit ($25.0\%$) to a safety-buffered MAD baseline ($28.0\%$). This accounts for real-world loop execution lag and sensor transmission delays.

### 4. Verification & Validation Methods
* **Risk Threshold Compliance:** Evaluated the final probability distribution array. Confirmed that the water shortage rate dropped to exactly $0.00\%$ under the smart schedule, validating that the feedback control loop works as intended.
* **Infrastructure Capacity Check:** Extracted the 95th percentile worst-case demand ($146.92\text{ mm/month}$). Cross-verified that this value safely falls below the physical water supply limitations of the farm's irrigation pumps.