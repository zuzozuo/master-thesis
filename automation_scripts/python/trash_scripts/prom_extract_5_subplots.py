import requests
import matplotlib.pyplot as plt
import pandas as pd
import time 
# Replace with your Prometheus server URL
prometheus_url = "http://10.20.20.60:9090/api/v1/query_range"

# Define the different time ranges and corresponding queue lengths
time_ranges = [
    ("2024-09-01T13:05:03Z", "2024-09-01T13:22:00Z", "queue length=1"),
    ("2024-09-01T14:36:03Z", "2024-09-01T14:52:00Z", "queue length=4"),
    ("2024-09-01T16:07:03Z", "2024-09-01T16:23:00Z", "queue length=10"),
    ("2024-09-01T17:38:03Z", "2024-09-01T17:51:00Z", "queue length=100"),
    ("2024-09-01T19:09:03Z", "2024-09-01T19:25:00Z", "queue length=200")
]

# Define your Prometheus query
query = 'perftest_latency_seconds{quantile="0.99"}'  # Replace with your actual Prometheus query

# Create subplots
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for i, (start_time, end_time, legend_label) in enumerate(time_ranges):
    # Optional: sleep for a bit to avoid overwhelming the server
    time.sleep(2)  # Sleep for 2 seconds between requests

    # Construct the query URL
    url = f"{prometheus_url}?query={query}&start={start_time}&end={end_time}&step=10s"
    
    # Send the request to Prometheus
    response = requests.get(url)
    data = response.json()

    # Check if the response contains data
    if 'data' not in data or 'result' not in data['data'] or len(data['data']['result']) == 0:
        print(f"No data returned for time range {start_time} to {end_time}. Skipping...")
        continue
    
    # Parse the response
    timestamps = []
    values = []
    
    for result in data['data']['result']:
        for value in result['values']:
            # Interpret the timestamp as milliseconds
            timestamps.append(pd.to_datetime(value[0], unit='ms'))
            values.append(float(value[1]))

    # Check if timestamps list is empty
    if not timestamps:
        print(f"No timestamps found for time range {start_time} to {end_time}. Skipping...")
        continue
    
    # Normalize the time by subtracting the first timestamp to align at t=0 seconds
    initial_time = timestamps[0]
    normalized_times = [(time - initial_time).total_seconds() for time in timestamps]
    
    # Convert to a Pandas DataFrame
    df = pd.DataFrame({"Time (s)": normalized_times, "Value": values})
    
    # Plot each time range in a separate subplot
    axes[i].plot(df["Time (s)"], df["Value"], label=legend_label)
    axes[i].fill_between(df["Time (s)"], df["Value"], alpha=0.3)
    axes[i].set_title(legend_label)
    axes[i].set_xlabel("Time (seconds)")
    axes[i].set_ylabel("Latency (seconds)")
    axes[i].legend(loc="center left", bbox_to_anchor=(1, 0.5))
    axes[i].grid(True)

# Hide the empty subplot (if any)
if len(time_ranges) < len(axes):
    fig.delaxes(axes[-1])

# Adjust layout and show the plot
plt.tight_layout()
plt.suptitle("End-to-End Message Latency", fontsize=16, y=1.02)
plt.show()