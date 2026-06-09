
### Project Directory Structure

```plaintext
HydroSense-Kenya/
|-- data/
|   |-- raw/
|   |   |-- weather_daily.csv
|   |   |-- soil_sensor_data.csv
|   |   |-- crop_zone_parameters.csv
|   |-- processed/
|       |-- cleaned_irrigation_dataset.csv
|
|-- notebooks/
|   |-- Level_1_Problem_Framing.ipynb
|   |-- Level_2_Vectorization_and_Error.ipynb
|   |-- Level_3_Numerical_Methods.ipynb
|   |-- Level_4_Data_Analysis_and_Visualization.ipynb
|   |-- Level_5_Simulation_and_Optimization.ipynb
|   |-- Level_6_Final_Integration.ipynb
|
|-- src/
|   |-- data_cleaning.py
|   |-- numerical_methods.py
|   |-- simulation.py
|   |-- optimization.py
|   |-- visualization.py
|
|-- tests/
|   |-- test_root_finding.py
|   |-- test_integration.py
|   |-- test_linear_systems.py
|   |-- test_simulation.py
|
|-- reports/
|   |-- final_scientific_report.pdf
|   |-- presentation_slides.pdf
|
|-- AI_USE_LOG.md
|-- README.md     
```

### `requirements.txt`

This manifest locks down the required libraries and specific versions to prevent environment fragmentation or broken package dependency chains.

```text
numpy==1.26.4
scipy==1.12.0
pandas==2.2.1
matplotlib==3.8.3
pytest==8.0.2
seaborn==0.13.2

```


### `README.md`

This is your main project documentation file. Copy this markdown text into your root folder:

```markdown
# HydroSense-Kenya: Advanced Scientific Computing Framework

This repository hosts the data pipeline, numerical calculation suites, and predictive modeling frameworks engineered for the **ICS 2207 Scientific Computing Capstone Project**. The system couples real-world IoT soil metrics with daily atmospheric datasets to simulate water-balance dynamics and manage operational agricultural risks.


## 🚀 Getting Started

### 1. Prerequisites & Environment Setup
Ensure you have Python 3.10+ installed. Isolate your dependencies using a Python virtual environment to guarantee reproducibility:

```bash
# Clone the repository and navigate to the root directory
cd hydrosense_kenya

# Initialize the virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows (Command Prompt):
venv\Scripts\activate.bat

```

### 2. Install Dependencies

Install all required scientific computing libraries using the locked `requirements.txt` manifest:

```bash
pip install --upgrade pip
pip install -r requirements.txt

```


## Core Architecture & Modules

* **`src/data_cleaning.py`**: Reads, normalizes, and cleans deliberate sensor data-entry anomalies (such as missing `NA` records or text-based flags) without breaking uniform step sequences.
* **`src/integration.py`**: Computes total cumulative rainfall records using the **Trapezoidal Rule** and a custom **Composite Simpson's 1/3 Mix** adapted to evaluate odd total interval counts ($n=29$).
* **`src/linear_systems.py`**: Assembles a tridiagonal flow coefficient matrix $Ax = b$ and uses **LU Decomposition with Partial Pivoting** to calculate interconnected water distribution across three farm zones.
* **`src/simulation.py`**: Houses the **1st-Order Euler** and **4th-Order Runge-Kutta (RK4)** numerical tracking loops to forecast soil-moisture depletion using multi-path weather inputs.


## Verification & Automated Testing

This framework utilizes **PyTest** to audit mathematical accuracy, boundary limits, and anomaly exception handling.

To execute the verification diagnostics and verify your math modules are working exactly as intended, run the following command from the project root:

```bash
pytest -v

```

## Compliance and Auditing

To maintain complete academic transparency, all interactive prompts, framework modifications, and mathematical validation methods utilized during the construction of this framework are logged chronologically inside `docs/AI_USE_LOG.md`.