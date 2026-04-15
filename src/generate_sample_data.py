import os
import numpy as np
import pandas as pd

np.random.seed(42)

def generate_test_run(filename, aggressive=False):
    time = np.arange(0, 120, 0.5)
    n = len(time)

    throttle = np.zeros(n)
    brake = np.zeros(n)
    speed = np.zeros(n)
    accel = np.zeros(n)
    distance = np.zeros(n)
    battery_voltage = np.zeros(n)
    battery_current = np.zeros(n)
    motor_torque = np.zeros(n)
    ambient_temp = 25 + 0.5 * np.sin(time / 20)

    for i, t in enumerate(time):
        if 5 <= t < 25:
            throttle[i] = 70 if not aggressive else 90
        elif 40 <= t < 55:
            throttle[i] = 45
        elif 75 <= t < 90:
            throttle[i] = 60 if not aggressive else 80
        else:
            throttle[i] = 0

        if 30 <= t < 36:
            brake[i] = 50
        elif 95 <= t < 102:
            brake[i] = 70 if aggressive else 55
        else:
            brake[i] = 0

    for i in range(1, n):
        drive_force = throttle[i] * 0.045
        brake_force = brake[i] * 0.09
        drag = 0.015 * speed[i - 1]
        accel[i] = drive_force - brake_force - drag + np.random.normal(0, 0.03)
        speed[i] = max(0, speed[i - 1] + accel[i] * 0.5)
        distance[i] = distance[i - 1] + speed[i] * 0.5
        motor_torque[i] = throttle[i] * 2.2 + np.random.normal(0, 3)
        battery_voltage[i] = 355 - 0.03 * battery_current[i - 1] + np.random.normal(0, 0.5)
        battery_current[i] = throttle[i] * 1.8 - brake[i] * 0.3 + np.random.normal(0, 2)

    speed_kph = speed * 3.6
    power_kw = (battery_voltage * battery_current) / 1000

    df = pd.DataFrame({
        "time_s": time,
        "speed_kph": speed_kph,
        "accel_mps2": accel,
        "throttle_pct": throttle,
        "brake_pct": brake,
        "battery_voltage_V": battery_voltage,
        "battery_current_A": battery_current,
        "motor_torque_Nm": motor_torque,
        "distance_m": distance,
        "ambient_temp_C": ambient_temp,
        "battery_power_kW": power_kw,
    })

    df.loc[20, "battery_current_A"] = np.nan
    df.loc[100, "speed_kph"] = np.nan

    os.makedirs("data/raw", exist_ok=True)
    df.to_csv(filename, index=False)
    print(f"Saved {filename}")

if __name__ == "__main__":
    generate_test_run("data/raw/test_run_01.csv", aggressive=False)
    generate_test_run("data/raw/test_run_02.csv", aggressive=True)