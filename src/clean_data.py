import os
import pandas as pd

def clean_vehicle_data(input_path, output_path):
    df = pd.read_csv(input_path)

    df = df.interpolate(method="linear")

    for col in ["speed_kph", "throttle_pct", "brake_pct"]:
        df[col] = df[col].clip(lower=0)

    df["accel_mps2_filtered"] = df["accel_mps2"].rolling(window=5, min_periods=1).mean()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned file saved to {output_path}")

if __name__ == "__main__":
    clean_vehicle_data("data/raw/test_run_01.csv", "data/processed/test_run_01_clean.csv")
    clean_vehicle_data("data/raw/test_run_02.csv", "data/processed/test_run_02_clean.csv")