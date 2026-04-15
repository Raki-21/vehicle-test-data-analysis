import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_zero_to_target_time(df, target_kph=50):
    reached = df[df["speed_kph"] >= target_kph]
    if reached.empty:
        return np.nan
    return reached.iloc[0]["time_s"]

def calculate_braking_distance(df):
    brake_events = df[df["brake_pct"] > 10]
    if brake_events.empty:
        return np.nan

    start_idx = brake_events.index[0]
    start_distance = df.loc[start_idx, "distance_m"]

    stopped = df[(df.index >= start_idx) & (df["speed_kph"] < 1)]
    if stopped.empty:
        return np.nan

    stop_distance = stopped.iloc[0]["distance_m"]
    return stop_distance - start_distance

def calculate_energy_kwh(df):
    dt = df["time_s"].diff().fillna(0)
    energy_kwh = (df["battery_power_kW"] * dt / 3600).sum()
    return energy_kwh

def calculate_kpis(df, run_name):
    return {
        "run_name": run_name,
        "max_speed_kph": df["speed_kph"].max(),
        "avg_speed_kph": df["speed_kph"].mean(),
        "peak_accel_mps2": df["accel_mps2_filtered"].max(),
        "peak_decel_mps2": df["accel_mps2_filtered"].min(),
        "zero_to_50_s": calculate_zero_to_target_time(df, 50),
        "braking_distance_m": calculate_braking_distance(df),
        "energy_used_kwh": calculate_energy_kwh(df),
        "max_motor_torque_Nm": df["motor_torque_Nm"].max(),
    }

def plot_run(df, run_name, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(10, 5))
    plt.plot(df["time_s"], df["speed_kph"])
    plt.xlabel("Time (s)")
    plt.ylabel("Speed (km/h)")
    plt.title(f"Speed vs Time - {run_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{run_name}_speed.png"))
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(df["time_s"], df["accel_mps2_filtered"])
    plt.xlabel("Time (s)")
    plt.ylabel("Filtered Acceleration (m/s²)")
    plt.title(f"Acceleration vs Time - {run_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{run_name}_acceleration.png"))
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(df["time_s"], df["battery_power_kW"])
    plt.xlabel("Time (s)")
    plt.ylabel("Battery Power (kW)")
    plt.title(f"Battery Power vs Time - {run_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{run_name}_battery_power.png"))
    plt.close()

def main():
    files = {
        "test_run_01": "data/processed/test_run_01_clean.csv",
        "test_run_02": "data/processed/test_run_02_clean.csv",
    }

    all_kpis = []

    for run_name, path in files.items():
        df = pd.read_csv(path)
        kpis = calculate_kpis(df, run_name)
        all_kpis.append(kpis)
        plot_run(df, run_name, "outputs/figures")

    kpi_df = pd.DataFrame(all_kpis)
    os.makedirs("outputs/kpis", exist_ok=True)
    kpi_df.to_csv("outputs/kpis/vehicle_test_kpis.csv", index=False)

    print(kpi_df)
    print("KPI file saved to outputs/kpis/vehicle_test_kpis.csv")

if __name__ == "__main__":
    main()