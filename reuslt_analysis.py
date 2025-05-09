import pandas as pd
import numpy as np

file_path = "./wan_result/test4.txt"

# Read CSV file (skip first row sync_offset)
with open(file_path, "r") as f:
    lines = f.readlines()

# Extract sync_offset (first line value)
sync_offset = float(lines[0].strip().split(",")[1])

# Read data starting from second row (actual CSV)
df = pd.read_csv(file_path, skiprows=1)

# Convert seconds to milliseconds
sync_offset_ms = sync_offset * 1000
df["latency_ms"] = df["latency"] * 1000
df["jitter_ms"] = df["jitter"] * 1000

# Calculate packet count
packet_count = len(df)

# Calculate raw statistics (ms)
latency_mean_raw = df["latency_ms"].mean()
latency_var_raw = df["latency_ms"].var()
jitter_mean_raw = df["jitter_ms"].mean()
jitter_var_raw = df["jitter_ms"].var()

# Calculate adjusted latency (ms)
df["latency_adjusted_ms"] = df["latency_ms"] - sync_offset_ms
latency_mean_adj = df["latency_adjusted_ms"].mean()
latency_var_adj = df["latency_adjusted_ms"].var()

# Print results
print(f"Sync Offset: {sync_offset_ms:.3f} ms")
print(f"Packet Count: {packet_count}")
print("\n--- Raw Statistics ---")
print(f"Latency (raw) - Mean: {latency_mean_raw:.3f} ms")
print(f"Latency (raw) - Variance: {latency_var_raw:.3f} ms²")
print(f"Jitter - Mean: {jitter_mean_raw:.3f} ms")
print(f"Jitter - Variance: {jitter_var_raw:.3f} ms²")
print("\n--- Adjusted Statistics (latency - sync_offset) ---")
print(f"Latency (adjusted) - Mean: {latency_mean_adj:.3f} ms")
print(f"Latency (adjusted) - Variance: {latency_var_adj:.3f} ms²")

# Fixed detailed statistics without deprecation warning
print("\n--- Detailed Statistics ---")
stats = df[["latency_ms", "jitter_ms"]].describe()
for col in stats.columns:
    stats[col] = stats[col].apply(lambda x: f"{x:.3f}")
print(stats)