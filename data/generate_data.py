import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

# ------------------- CONFIG -------------------
NUM_DEVICES = 20
LOCATIONS = ['Mumbai', 'Chennai', 'Delhi', 'Kolkata', 'Hyderabad']
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)
OUTPUT_PATH = 'data/oee_data.xlsx'

# ------------------ HELPERS -------------------
def generate_device_id(index):
    return f"PKG-{index:03d}"

def get_ideal_cycle_time(device_id):
    # Simulate different speeds for different machines
    base = 0.5 + (int(device_id.split('-')[1]) % 5) * 0.1
    return round(base + np.random.uniform(-0.05, 0.05), 2)

# ------------------ MAIN LOGIC -------------------
print("Generating synthetic OEE data...")

device_ids = [generate_device_id(i) for i in range(1, NUM_DEVICES + 1)]
date_range = pd.date_range(start=START_DATE, end=END_DATE, freq='D')
records = []

for date in date_range:
    for device in device_ids:
        location = random.choice(LOCATIONS)
        total_output = np.random.randint(1000, 3000)  # Varies per shift
        good_output = int(total_output * np.random.uniform(0.90, 0.99))
        downtime = np.random.randint(10, 180)  # in minutes
        ideal_cycle_time = get_ideal_cycle_time(device)
        operating_time = max(480 - downtime, 0)  # prevent negative time

        records.append({
            'Timestamp': date,
            'Device ID': device,
            'Location': location,
            'Total Output': total_output,
            'Good Output': good_output,
            'Downtime (min)': downtime,
            'Ideal Cycle Time (s)': ideal_cycle_time,
            'Operating Time (min)': operating_time
        })

# ------------------ SAVE TO EXCEL -------------------
df = pd.DataFrame(records)
os.makedirs('data', exist_ok=True)
df.to_excel(OUTPUT_PATH, index=False)
print(f"✅ Data generated and saved to '{OUTPUT_PATH}' with {len(df):,} records.")
