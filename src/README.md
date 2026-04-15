# Vehicle Test Data Analysis

## Overview
This project analyzes simulated vehicle longitudinal test data using Python. The goal was to build a testing-oriented workflow for cleaning raw signals, calculating key performance indicators (KPIs), comparing test runs, and generating engineering plots.

## Project Objective
The purpose of this project was to simulate a basic automotive vehicle test data analysis workflow relevant to vehicle testing, validation, and e-mobility engineering roles.

## Tools Used
- Python
- Pandas
- NumPy
- Matplotlib

## Data Signals Included
- Time
- Speed
- Acceleration
- Throttle input
- Brake input
- Battery voltage
- Battery current
- Motor torque
- Distance
- Ambient temperature
- Battery power

## Workflow
1. Generated simulated vehicle test run data
2. Cleaned missing and noisy values
3. Applied basic signal smoothing
4. Calculated vehicle performance KPIs
5. Generated engineering plots
6. Exported KPI summary as CSV

## Key KPIs
- Maximum speed
- Average speed
- Peak acceleration
- Peak deceleration
- 0–50 km/h time
- Braking distance
- Estimated energy usage
- Maximum motor torque

## Outputs
### Figures
Saved in `outputs/figures`:
- Speed vs Time
- Acceleration vs Time
- Battery Power vs Time

### KPI Summary
Saved in `outputs/kpis/vehicle_test_kpis.csv`

## Project Structure
```text
vehicle-test-data-analysis
│
├── data
│   ├── raw
│   └── processed
├── outputs
│   ├── figures
│   └── kpis
├── src
│   ├── generate_sample_data.py
│   ├── clean_data.py
│   └── analyze_data.py
├── requirements.txt
└── README.md